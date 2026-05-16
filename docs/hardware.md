# Hardware

Inventory and capacity notes for the home lab hardware.

## Harvester Nodes

| Host | Role | IP | Primary Link | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `the-abundance` | Harvester physical node | `192.168.1.241` | 10G SFP+ | active | Verified Ready in Harvester |
| `the-elation` | Harvester physical node | `192.168.1.250` | 10G SFP+ | active | Verified Ready in Harvester |
| `the-enigmata` | Harvester physical node | `192.168.1.244` | 1G RJ45 via SFP/RJ45 module | active | Verified Ready in Harvester; replaces stale `the-remembrance` references |

## VM Sizing Baseline

| VM | vCPU | Memory | Disk | Notes |
| --- | ---: | ---: | ---: | --- |
| `cp-01` | 4 | 8 Gi | 100 Gi | Active Talos control-plane node on `the-abundance`; OS disk uses `slow` |
| `cp-02` | 4 | 8 Gi | 100 Gi | Active Talos control-plane node on `the-elation`; OS disk uses `slow` |
| `cp-03` | 4 | 8 Gi | 100 Gi | Active Talos control-plane node on `the-enigmata`; OS disk uses `slow` |
| `worker-01` | 4 | 12 Gi | 100 Gi | Active general Talos worker VM on `the-elation`; OS disk uses `slow` |
| `worker-02` | 2 | 8 Gi | 80 Gi | Active general Talos worker VM on `the-enigmata`; OS disk uses `slow` |
| `data-01` | 8 | 32 Gi | 100 Gi OS + 10 TiB data + 1 TiB hot/temp | Active tainted Talos data worker on `the-abundance`; `slow` for OS/data, `the-abundance-nvme` for hot/temp |

Add CPU, memory, disk, NIC, firmware, and BIOS notes here as the lab grows.
