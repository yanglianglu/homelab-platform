# Hardware

Inventory and capacity notes for the home lab hardware.

## Harvester Nodes

| Host | Role | IP | Primary Link | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `the-abundance` | Harvester physical node | `192.168.1.241` | 10G SFP+ | active | Current known Harvester node |
| `the-elation` | Harvester physical node | `TBD` | 10G SFP+ | planned | Intended second physical node |
| `the-remembrance` | Harvester physical node | `TBD` | 1G RJ45 via SFP/RJ45 module | planned | Intended third physical node |

## VM Sizing Baseline

| VM | vCPU | Memory | Disk | Notes |
| --- | ---: | ---: | ---: | --- |
| `talos-cp-01` | 4 | 8 Gi | 100 Gi | First Talos control-plane node on `the-abundance` |
| `talos-worker-01` | TBD | TBD | TBD | Planned worker VM on `the-elation` |
| `talos-worker-02` | TBD | TBD | TBD | Planned worker VM on `the-remembrance` |

Add CPU, memory, disk, NIC, firmware, and BIOS notes here as the lab grows.
