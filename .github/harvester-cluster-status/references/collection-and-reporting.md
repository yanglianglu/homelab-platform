# Collection And Reporting Reference

Use this reference when producing a full Harvester cluster status report. Commands are read-only. Skip any unavailable CRD/API with a note rather than trying a mutating workaround.

## Connection And Permission Checks

When on a Harvester/RKE2 node:

```bash
export PATH="$PATH:/var/lib/rancher/rke2/bin"
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml
```

Verify access:

```bash
kubectl auth can-i get nodes
kubectl auth can-i list pods -A
kubectl auth can-i get storageclasses
kubectl auth can-i get persistentvolumeclaims -A
kubectl auth can-i get virtualmachines.kubevirt.io -A
kubectl auth can-i get volumes.longhorn.io -n longhorn-system
```

## A. Cluster And Node Overview

```bash
kubectl get nodes -o wide
kubectl describe nodes
kubectl get componentstatuses 2>/dev/null || true
kubectl get --raw='/readyz?verbose' 2>/dev/null || true
kubectl get --raw='/livez?verbose' 2>/dev/null || true
kubectl top nodes 2>/dev/null || true
```

Summarize node count, Ready/NotReady, roles, internal IPs, Kubernetes/RKE2 version, OS/kernel/runtime, CPU/memory/disk/network pressure, network unavailable conditions, and recent node events.

## B. Namespace And Pod Health

```bash
kubectl get ns
kubectl get pods -A -o wide
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded -o wide
kubectl get events -A --sort-by='.lastTimestamp' | tail -100
kubectl top pods -A 2>/dev/null || true
```

Group by `kube-system`, `harvester-system`, `longhorn-system`, `cattle-system`, other `cattle-*` namespaces, `talos-cluster`, and other namespaces. Report Running/Pending/CrashLoopBackOff/Completed counts, restart-heavy pods, and suspicious warnings/events.

## C. RKE2/Kubernetes Control Plane

```bash
kubectl get pods -n kube-system -o wide
kubectl get endpoints -n default kubernetes
kubectl get leases -n kube-node-lease
kubectl get leases -n kube-system
```

Inspect etcd, kube-apiserver, kube-controller-manager, kube-scheduler, cloud-controller-manager, kube-proxy, CoreDNS, metrics-server, ingress-nginx, Canal, Multus, Whereabouts, and snapshot-controller.

## D. Harvester Platform

```bash
kubectl get pods -n harvester-system -o wide
kubectl get deploy -n harvester-system
kubectl get daemonset -n harvester-system
kubectl get jobs -n harvester-system
kubectl get svc -n harvester-system
kubectl get ingress -A
```

Summarize Harvester API/UI, webhooks, network controller, node disk manager, node manager, kube-vip, KubeVirt virt-api/controller/operator/handler, CDI components, and failed or restart-heavy pods.

## E. VIP And Management Endpoint

```bash
kubectl -n kube-system get svc ingress-expose -o yaml 2>/dev/null || true
kubectl -n harvester-system get pods -l app.kubernetes.io/name=kube-vip -o wide 2>/dev/null || true
kubectl -n harvester-system get pods | grep kube-vip || true
```

Extract requested VIP, VIP host/owner, VIP MAC/hwaddr annotation, kube-vip pod placement, and any mismatch between node IP access and VIP behavior. Do not change VIP settings.

## F. KubeVirt VM Layer

```bash
kubectl get virtualmachines.kubevirt.io -A
kubectl get virtualmachineinstances.kubevirt.io -A -o wide
kubectl get pods -A | grep virt-launcher || true
kubectl get datavolumes.cdi.kubevirt.io -A
kubectl get pvc -A
```

For each VM, identify namespace, name, printable status, running/stopped state, VMI node placement, launcher pod, disk PVCs, network attachments when visible, live migration status, and storage live migratable condition when visible.

For `talos-cluster`, identify current Talos VMs (`cp-*`, `worker-*`,
`data-01`), boot PVCs, current StorageClasses, whether each running VM has a
`virt-launcher` pod, and active DataVolume import/clone operations. Treat
`talos-cp-01` as retired unless it appears live.

## G. CDI And DataVolumes

```bash
kubectl get datavolumes.cdi.kubevirt.io -A
kubectl get storageprofile
kubectl get storageprofile -o yaml
```

Report DataVolumes in progress, clone/import phase, clone strategy per StorageProfile, stuck smart-clone/snapshot state, host-assisted copy pods, and whether StorageProfiles use snapshot or copy. Do not expose tokens or secret values from annotations.

## H. StorageClasses, PVCs, PVs, Snapshots

```bash
kubectl get storageclass
kubectl get storageclass -o yaml
kubectl get pvc -A
kubectl get pv
kubectl get volumesnapshot -A
kubectl get volumesnapshotclass
kubectl get volumesnapshotcontent
```

Group StorageClasses by default class, Longhorn defaults, Harvester VM classes, fast/NVMe classes, HA classes, VM state persistence, static classes, and node-specific classes. For each class, extract provisioner, reclaim policy, volume binding mode, expansion, `numberOfReplicas`, `diskSelector`, `nodeSelector`, `migratable`, `dataEngine`, `encrypted`, and `dataLocality`.

For PVCs, report namespace, name, status, capacity, access mode, volume mode, StorageClass, and attached workload when inferable.

## I. Longhorn

```bash
kubectl -n longhorn-system get pods -o wide
kubectl -n longhorn-system get nodes.longhorn.io
kubectl -n longhorn-system get nodes.longhorn.io -o yaml
kubectl -n longhorn-system get volumes.longhorn.io
kubectl -n longhorn-system get volumes.longhorn.io -o yaml
kubectl -n longhorn-system get replicas.longhorn.io
kubectl -n longhorn-system get engines.longhorn.io
kubectl -n longhorn-system get settings.longhorn.io
kubectl -n longhorn-system get recurringjobs.longhorn.io
kubectl -n longhorn-system get backingimages.longhorn.io
```

For Longhorn nodes, report Ready/schedulable state, disk paths, disk tags, node tags, `allowScheduling`, available/used/reserved storage, and conditions.

For Longhorn volumes, report state, robustness, replica count, actual size, frontend, attached node, backing image, and associated PVC/workload when inferable.

For replicas, identify degraded, missing, rebuilding, node distribution, and whether HA volumes have replicas across multiple eligible nodes.

## J. Network Layer

```bash
kubectl get network-attachment-definitions -A
kubectl get ippools -A 2>/dev/null || true
kubectl get pods -n kube-system -o wide | grep -E 'multus|whereabouts|canal|ingress|coredns' || true
kubectl get pods -n harvester-system -o wide | grep -E 'network|kube-vip' || true
```

Report Multus, Whereabouts, Canal, VM network attachment definitions, IP pools, and obvious IPAM or network-controller errors.

## K. Targeted Logs Only

Collect logs only for pods that are CrashLoopBackOff, Error, Failed, unexpectedly Pending, restart-heavy, or directly tied to an active failure:

```bash
kubectl logs -n <namespace> <pod> --tail=100
kubectl describe pod -n <namespace> <pod>
```

Use `--previous` only for containers that recently crashed. Do not collect broad logs from healthy pods.

## Interpretation Rules

- Treat `Completed` as normal for Jobs unless failed events say otherwise.
- Correlate restart counts with age and last restart time; old restarts may be historical.
- Treat PVC `Pending` as important only when it is expected to be `Bound`.
- Treat DataVolume `CloneInProgress` as normal during migration unless stuck by age/events/progress.
- Treat failed VolumeSnapshots as possibly stale; correlate with active DataVolumes.
- Remember that Longhorn replica count 3 improves availability but increases write amplification and network overhead.
- Verify `diskSelector=nvme` and node/disk tags before assuming a StorageClass can place replicas.
- Verify `numberOfReplicas=3` against the number of eligible Longhorn nodes/disks.
- Remember that VM disks are PVCs referenced in `spec.template.spec.volumes[*].persistentVolumeClaim.claimName`.
- Do not assume StorageClass changes affect existing PVCs; existing PVCs need clone/migration/recreation.

## Final Report Outline

1. Executive summary: overall health, top 3 findings, top 3 risks, immediate next checks.
2. Cluster topology: nodes, roles, IPs, Kubernetes/Harvester version, control-plane/etcd layout.
3. System health by layer: Kubernetes/RKE2, Harvester, KubeVirt, CDI, Longhorn, Network/VIP, Rancher/Fleet/Cattle, user workloads/VM namespaces.
4. Storage report: StorageClasses grouped by tier, Longhorn nodes/disks/tags, PVCs/PVs, volumes/replicas/robustness, snapshot status, migration/import/clone status.
5. VM report: VM list, running/stopped state, VMI placement, disk PVC mapping, StorageClass mapping, migration readiness if visible.
6. Warning and anomaly report: pending pods/PVCs, failed snapshots, degraded volumes, restart-heavy pods, node pressure, network/VIP inconsistencies.
7. Recommendations: read-only validation steps, operational risks, suggested future changes clearly labeled as recommendations only.
8. Appendix: commands executed, summarized raw outputs, commands skipped for safety.
