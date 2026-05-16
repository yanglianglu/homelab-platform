# Talos Worker VMs

This directory owns Harvester-side desired state and sizing notes for Talos worker VMs.

Initial worker target:

| VM | Host | IP | Size | Status |
| --- | --- | --- | --- | --- |
| `worker-01` | `the-elation` | `192.168.1.179` | 4 CPU / 12 Gi | planned |
| `worker-02` | `the-enigmata` | `192.168.1.180` | 2 CPU / 8 Gi | planned |
| `worker-03` | TBD | TBD | TBD | deferred |

Do not create `worker-03` until real scheduling pressure or workload metrics justify it.
