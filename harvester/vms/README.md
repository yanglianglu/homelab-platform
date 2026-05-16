# Harvester VM Desired State

This directory separates VM ownership by workload family.

| Directory | Owns |
| --- | --- |
| `talos/control-plane/` | Talos control-plane VMs such as `cp-01`, `cp-02`, and `cp-03` |
| `talos/workers/` | Talos worker VMs such as `worker-01`, `worker-02`, and future workers |
| `data/` | Dedicated data workload VMs such as `data-01` |

Only commit cleaned desired-state manifests or planning notes. Do not commit live exports with runtime metadata, generated secrets, cloud-init payloads, or status fields.
