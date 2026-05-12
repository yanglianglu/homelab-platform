# whoami

`whoami` is the first app-path GitOps smoke test for the homelab cluster.

It proves that a Git change can flow through GitHub, Argo CD, and Kubernetes
into a running workload in the `apps` namespace.

## Scope

- Argo CD Application: `apps-whoami`
- Argo CD project: `apps`
- Namespace: `apps`
- Service type: `ClusterIP`
- Secrets: none
- Ingress/TLS: deferred to Stage 4

## Verification

```sh
kubectl --context homelab-talos -n argocd get application apps-whoami
kubectl --context homelab-talos -n apps get deploy,pod,svc -l app.kubernetes.io/name=whoami
kubectl --context homelab-talos -n apps port-forward svc/whoami 8081:80
```

Then, from another terminal:

```sh
curl http://127.0.0.1:8081/
```
