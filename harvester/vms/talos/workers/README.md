# Talos Worker VMs

This directory owns Harvester-side desired state and sizing notes for Talos worker VMs.

Current worker set:

| VM | Host | IP | Size | Status |
| --- | --- | --- | --- | --- |
| `worker-01` | `the-elation` | `192.168.1.179` | 4 CPU / 12 Gi | active |
| `worker-02` | `the-enigmata` | `192.168.1.180` | 2 CPU / 8 Gi | active |
| `data-01` | `the-abundance` | `192.168.1.185` | 8 CPU / 32 Gi | active data worker |
| `worker-03` | TBD | TBD | TBD | deferred |

Do not create `worker-03` until real scheduling pressure or workload metrics justify it.

`data-01` is not general worker capacity. It is pinned to `the-abundance`,
tainted `data-platform=true:NoSchedule`, and uses a CSI-first storage model.
The legacy 10 TiB and 1 TiB PVCs are detached from the VM and retained only as
rollback until a separate cleanup gate deletes them.
