---
name: harvester-cluster-status
description: Read-only Harvester v1.8.x, RKE2, KubeVirt, CDI, Longhorn, Multus, and Rancher/Fleet cluster status analysis. Use when Codex needs to connect to a Harvester Kubernetes cluster with read-only API calls, collect node/pod/storage/VM/network/event health, inspect Talos VM namespaces such as talos-cluster, and produce a structured operational report without remediation or mutation.
---

# Harvester Cluster Status

## Mission

Observe and explain the current state of a Harvester cluster. Produce a concise but complete technical report covering physical nodes, RKE2 control plane, Harvester services, KubeVirt VMs, CDI/DataVolumes, Longhorn storage, networking/VIP, events, risks, and read-only next checks.

Use `references/collection-and-reporting.md` for the full command matrix, interpretation notes, and report outline. Use `scripts/collect_harvester_status.sh` when broad read-only collection is useful and shell access to a configured `kubectl` is available.

## Safety Contract

Perform observation only.

- Do not run mutating `kubectl` verbs or subcommands, including `apply`, `create`, `delete`, `edit`, `patch`, `replace`, `scale`, `cordon`, `drain`, `taint`, `label`, `annotate`, `exec`, `cp`, `port-forward`, `rollout restart`, or upgrade commands.
- Do not modify StorageClasses, PVCs, Longhorn volumes, VMs, snapshots, nodes, labels, taints, settings, or VM power/migration/snapshot/backup state.
- Do not read or print Secret data values. Do not run `kubectl get secret -o yaml/json`, decode secret data, or print tokens, passwords, kubeconfigs, certificates, or private keys.
- Allow only read-only operations: API discovery, `auth can-i`, `get`, `describe`, `logs`, `top`, `kubectl get --raw` health checks, and local filtering/summarization.
- If a requested command may mutate the cluster, skip it and state why in the report appendix.

## Workflow

1. Establish access.
   - If running on a Harvester/RKE2 node and no kubeconfig is set, use `/var/lib/rancher/rke2/bin` on `PATH` and `/etc/rancher/rke2/rke2.yaml` as `KUBECONFIG` only if readable.
   - If running remotely, use the provided kubeconfig/context.
   - Verify permissions with `kubectl auth can-i get nodes`, `list pods -A`, `get storageclasses`, `get persistentvolumeclaims -A`, `get virtualmachines.kubevirt.io -A`, and `get volumes.longhorn.io -n longhorn-system`.

2. Collect read-only data.
   - Prefer the bundled collector for full status snapshots:
     ```bash
     bash scripts/collect_harvester_status.sh --output-dir ./harvester-status
     ```
   - Add `--context <name>` or `--kubeconfig <path>` when needed.
   - Use manual commands from `references/collection-and-reporting.md` if the collector is not suitable.

3. Inspect targeted logs only.
   - Collect logs and `describe pod` output only for pods that are failing, pending unexpectedly, CrashLooping, Error/Failed, restart-heavy, or directly related to an active anomaly.
   - Use `--tail=100`; do not dump broad logs from healthy components.

4. Analyze by layer.
   - Cluster/node health: readiness, roles, versions, OS/kernel/runtime, pressure, disk/network conditions, node events.
   - RKE2/Kubernetes: etcd, API server, controller manager, scheduler, cloud controller, CoreDNS, kube-proxy, Canal, Multus, metrics-server, ingress, snapshot controllers, leases/endpoints.
   - Harvester: API/UI, webhooks, network controller, node manager, node disk manager, kube-vip, KubeVirt, CDI, services, ingress, jobs.
   - KubeVirt/VMs: VM/VMI status, placement, launcher pods, disks/PVCs, networks, migration readiness when visible.
   - CDI/DataVolumes: import/clone phases, StorageProfiles, clone strategy, smart-clone/snapshot/copy state, host-assisted pods.
   - Longhorn: manager/engine/instance-manager pods, Longhorn nodes/disks/tags/capacity, volumes/robustness/replicas/engines, settings, recurring jobs, backing images.
   - Network/VIP: kube-vip owner/placement, management service VIP data, Multus, Whereabouts, Canal, network attachment definitions, IP pools.
   - Workload namespaces: especially `talos-cluster`, current Talos VMs
     (`cp-*`, `worker-*`, `data-01`), and retired `talos-cp-01` only if present.

5. Correlate before judging.
   - Treat `Completed` pods as normal for jobs unless events indicate failure.
   - Treat old restarts as historical unless recent restart time/events show active churn.
   - Treat PVC `Pending` as important only if it should already be bound.
   - Treat DataVolume `CloneInProgress` as possibly normal; check age, progress, PVC binding, importer/clone pods, and snapshot events.
   - Treat stale failed VolumeSnapshots as historical unless an active DataVolume or VM operation still depends on them.
   - Verify that Longhorn replica count and StorageClass selectors can actually place replicas across eligible nodes/disks.

## Report Shape

Return the final answer as a concise technical report with these sections:

1. Executive summary: overall health (`Healthy`, `Degraded`, `Critical`, or `Unknown`), top 3 findings, top 3 risks, immediate next checks.
2. Cluster topology: nodes, roles, IPs, Kubernetes/Harvester version, control-plane/etcd layout.
3. System health by layer: Kubernetes/RKE2, Harvester, KubeVirt, CDI, Longhorn, Network/VIP, Rancher/Fleet/Cattle, user workload/VM namespaces.
4. Storage report: StorageClasses by tier, Longhorn nodes/disks/tags, PVCs/PVs, volumes/replicas/robustness, snapshots, migration/import/clone status.
5. VM report: VM list, running/stopped state, VMI placement, disk PVC mapping, StorageClass mapping, migration readiness if visible.
6. Warning and anomaly report: pending pods/PVCs, failed snapshots, degraded Longhorn volumes, restart-heavy pods, node pressure, network/VIP inconsistencies.
7. Recommendations: read-only validation steps, operational risks, suggested future changes clearly labeled as recommendations only.
8. Appendix: commands executed, summarized raw outputs, commands skipped for safety.

## Output Discipline

- Summarize raw command output instead of pasting large YAML, pod lists, or logs.
- Include exact object names, namespaces, nodes, StorageClasses, PVCs, Longhorn volumes, and event messages when they support a finding.
- Never expose secret data. If Secret names are relevant, mention names/types/ages only.
- Do not perform remediation. Suggested changes belong only in the recommendations section.
