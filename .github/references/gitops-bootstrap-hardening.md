# GitOps Bootstrap Hardening Notes

This reference captures the practical lessons from bringing the homelab
`homelab-talos` GitOps path from broken sync to a working app deployment.

It is written for future operators and Codex sessions. Treat it as the
first-response checklist before changing Argo CD, External Secrets, or the first
application paths.

## Current Baseline

- Cluster context: `homelab-talos`
- Argo CD namespace: `argocd`
- Root Application: `homelab-root`
- Root Git path: `kubernetes/clusters/homelab`
- Git branch tracked by Argo CD: `main`
- App workload namespace: `apps`
- First app-path smoke test: `apps-whoami`
- Repo credential source: Infisical through External Secrets Operator
- Repo credential target Secret: `argocd/argocd-github-app-repo-creds`

Expected steady state:

```sh
kubectl --context homelab-talos -n argocd get applications.argoproj.io
```

The core Applications should be `Synced` and `Healthy`, including:

- `homelab-root`
- `platform-external-secrets`
- `platform-infisical`
- `platform-argocd-repo-access`
- `platform-namespaces`
- `platform-policies`
- `apps-whoami`

## What Happened

The original Argo CD sync error was not caused by Kubernetes workload failure.
It was caused by live Argo CD Application objects pointing at stale Git paths
after the repository layout changed.

Bad live paths included:

- `kubernetes/clusters/homelab/argocd`
- `kubernetes/clusters/homelab/platform/namespaces`
- `kubernetes/clusters/homelab/platform/policies`
- `kubernetes/clusters/homelab/platform/secrets`

The corrected paths are capability-numbered and rooted under:

- `kubernetes/clusters/homelab`
- `kubernetes/clusters/homelab/platform/00-namespaces`
- `kubernetes/clusters/homelab/platform/20-infisical`
- `kubernetes/clusters/homelab/platform/30-argocd-repo-access`
- `kubernetes/clusters/homelab/platform/40-policies`

The immediate fix was to apply the current root Application from Git:

```sh
kubectl --context homelab-talos apply \
  -f kubernetes/bootstrap/argocd/root/homelab-root-application.yaml
```

That let `homelab-root` reconcile the new app-of-apps layout.

## Argo CD Application Placement

Argo CD `Application` resources are control-plane objects. In this repo they
live in the `argocd` namespace even when the workloads they manage deploy
elsewhere.

Example:

```yaml
metadata:
  name: apps-whoami
  namespace: argocd
spec:
  destination:
    namespace: apps
```

This means:

- `apps-whoami` is watched by Argo CD in `argocd`.
- `Deployment/whoami`, `Service/whoami`, and `Pod/whoami` live in `apps`.
- Control objects and app workloads stay separated by namespace.

## External Secrets Drift

`platform-argocd-repo-access` initially stayed `OutOfSync` even after sync
operations succeeded.

Cause: External Secrets Operator defaulted fields onto the live
`ExternalSecret`, while the Git manifest omitted them. Argo CD saw this as
drift and kept self-healing.

The fix was to make those defaults explicit in Git:

```yaml
spec:
  target:
    creationPolicy: Owner
    deletionPolicy: Retain
    template:
      engineVersion: v2
      mergePolicy: Replace
  data:
    - remoteRef:
        conversionStrategy: Default
        decodingStrategy: None
        metadataPolicy: None
        nullBytePolicy: Ignore
```

Lesson: when an operator writes stable default fields to a managed resource,
prefer making those defaults explicit in Git instead of fighting continuous
Argo CD drift.

## whoami Smoke App

The first app-path proof is `apps/whoami`.

Its purpose is intentionally narrow:

- prove GitHub to Argo CD to Kubernetes works
- use the real `apps` AppProject path
- avoid external routing, TLS, and secrets
- expose only a `ClusterIP` Service

Useful checks:

```sh
kubectl --context homelab-talos -n argocd get application apps-whoami
kubectl --context homelab-talos -n apps get deploy,pod,svc \
  -l app.kubernetes.io/name=whoami -o wide
kubectl --context homelab-talos -n apps rollout status deployment/whoami
kubectl --context homelab-talos -n apps port-forward svc/whoami 18081:80
curl http://127.0.0.1:18081/
```

## Security Context Pattern

The `whoami` pod uses both pod-level and container-level `securityContext`.

Pod-level settings define defaults for the whole pod:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 65532
  runAsGroup: 65532
  seccompProfile:
    type: RuntimeDefault
```

Container-level settings constrain the individual container:

```yaml
securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
```

Because the container runs as non-root, it listens on `8080` internally:

```yaml
args:
  - --port=8080
ports:
  - name: http
    containerPort: 8080
```

The Service still exposes normal HTTP port `80` inside the cluster:

```yaml
ports:
  - name: http
    port: 80
    targetPort: http
```

## Single-Node Scheduling Reality

Historical bootstrap note: the cluster originally had one node, `cp-01`, with
the standard control-plane taint:

```text
node-role.kubernetes.io/control-plane:NoSchedule
```

Normal app pods will not schedule there unless they tolerate that taint.

At that time, the `whoami` smoke test used this toleration:

```yaml
tolerations:
  - key: node-role.kubernetes.io/control-plane
    operator: Exists
    effect: NoSchedule
```

This was a pragmatic single-node bootstrap exception. Worker nodes now exist,
so regular app workloads should schedule onto workers unless a new bootstrap or
repair gate explicitly approves a control-plane toleration.

## Debugging Checklist

Start with Argo CD status:

```sh
kubectl --context homelab-talos -n argocd get applications.argoproj.io -o wide
```

If an app is `Unknown`, describe it and look for comparison errors:

```sh
kubectl --context homelab-talos -n argocd describe application homelab-root
```

Common root causes:

- live Application points at a deleted Git path
- Argo CD is still comparing an old revision
- operator default fields cause Argo CD drift
- AppProject destination or source repo does not allow the child app
- pod is synced but unscheduled because of node taints

Force refresh after pushing to `main`:

```sh
kubectl --context homelab-talos -n argocd annotate application homelab-root \
  argocd.argoproj.io/refresh=hard --overwrite
```

Refresh a child app directly:

```sh
kubectl --context homelab-talos -n argocd annotate application apps-whoami \
  argocd.argoproj.io/refresh=hard --overwrite
```

Validate locally before pushing:

```sh
kubectl kustomize kubernetes/clusters/homelab
kubectl kustomize kubernetes/clusters/homelab/apps/whoami/app
kubectl --context homelab-talos apply --dry-run=server \
  -k kubernetes/clusters/homelab/apps/whoami/app
```

## Branch And Git Rules

Argo CD tracks `main`. If a fix is made on another branch, it will not affect
the cluster until it reaches `main`.

Before a cluster-facing change:

```sh
git status --short --branch
git fetch origin
git switch main
git pull --ff-only origin main
```

After pushing:

```sh
git push origin main
kubectl --context homelab-talos -n argocd annotate application homelab-root \
  argocd.argoproj.io/refresh=hard --overwrite
```

## Linear Trail

Relevant completed issues:

- `FIF-23`: Install Argo CD and bootstrap root app
- `FIF-18`: Choose initial secrets approach for GitOps
- `FIF-24`: Install External Secrets Operator and sync test secret
- `FIF-26`: Manage Argo CD GitHub App repo credential with Infisical and ESO
- `FIF-17`: Deploy whoami test app from GitOps

Remaining follow-up themes:

- create/finish Linear execution views
- decide admin VPN access pattern
- define internal DNS and Gateway address model
- install Gateway API, Envoy Gateway, cert-manager, and trust-manager
- protect the first dashboard or app with identity-aware access
