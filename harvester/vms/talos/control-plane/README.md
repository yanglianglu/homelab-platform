# Talos Control-Plane VMs

This directory owns Harvester-side desired state for Talos control-plane VMs.

| VM | Host | IP | Status | Notes |
| --- | --- | --- | --- | --- |
| `cp-01` | `the-abundance` | `192.168.1.181` | active | Control-plane VM |
| `cp-02` | `the-elation` | `192.168.1.182` | active | Control-plane VM |
| `cp-03` | `the-enigmata` | `192.168.1.183` | active | Control-plane VM |

Control-plane VMs use `slow` OS disks as rebuildable disks. Kubernetes API
clients should use the stable kube-vip endpoint `192.168.1.184`; individual
node IPs remain break-glass endpoints.
