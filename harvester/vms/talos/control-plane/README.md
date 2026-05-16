# Talos Control-Plane VMs

This directory owns Harvester-side desired state for Talos control-plane VMs.

| VM | Host | IP | Status | Notes |
| --- | --- | --- | --- | --- |
| `cp-01` | `the-abundance` | `192.168.1.181` | active | Existing single control-plane VM |
| `cp-02` | `the-elation` | `192.168.1.182` | planned | Create only after `cp-01` API reachability is understood |
| `cp-03` | `the-enigmata` | `192.168.1.183` | planned | Create only after `cp-02` join path is validated |

Control-plane VMs use `slow` OS disks as rebuildable disks. Kubernetes API clients should eventually use a stable API VIP instead of one node IP.
