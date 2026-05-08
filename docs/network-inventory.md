# Network Inventory

This file is the lightweight source of truth for current and planned home lab network devices. It is intentionally simple enough to maintain in Git before adding a heavier inventory tool such as NetBox.

## Current Topology

```text
Internet
  -> AT&T Router
  -> USW-Aggregation
      -> the-abundance
      -> the-elation
      -> the-remembrance
```

No dedicated firewall is planned at this stage. The AT&T router remains the gateway.

## Devices

| Device | Role | Management IP | Platform / Model | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `att-router` | Router / gateway | `192.168.1.254` | AT&T Fiber Router | active | Current default gateway |
| `usw-aggregation` | 10G aggregation switch | `TBD` | UniFi USW-Aggregation | not set up | Connected directly to AT&T router |
| `the-abundance` | Physical Harvester node | `192.168.1.241` | TBD | active | Hosts current Harvester environment and `talos-cp-01` |
| `the-elation` | Physical Harvester node | `TBD` | TBD | planned | Intended second physical node |
| `the-remembrance` | Physical Harvester node | `TBD` | TBD | planned | Intended third physical node |
| `harvester-vip` | Harvester UI/API VIP | `192.168.1.50` | Harvester VIP | active | Shared Harvester access IP |
| `talos-cp-01` | Talos control-plane VM | `192.168.1.178` | Talos v1.13.0 | active | Bootstrapped and healthy |
| `talos-worker-01` | Talos worker VM | `TBD` | Talos v1.13.0 | planned | One worker VM on `the-elation` |
| `talos-worker-02` | Talos worker VM | `TBD` | Talos v1.13.0 | planned | One worker VM on `the-remembrance` |

## Node Link Plan

| Node | Link Type | Target Speed | Switch Port | Cable / Adapter | Notes |
| --- | --- | ---: | --- | --- | --- |
| `the-abundance` | SFP+ | 10G | `sfp1` | DAC | Direct SFP+ preferred |
| `the-elation` | SFP+ | 10G | `sfp2` | DAC | Direct SFP+ preferred |
| `the-remembrance` | RJ45 | 1G | `sfp3` | SFP-to-RJ45 module | USW-Aggregation is SFP+, so RJ45 requires a transceiver/module |
| `att-router` | RJ45 | likely 1G | `sfp8` | SFP-to-RJ45 module | Uplink to current gateway |

## Open Items

- Assign management IPs for `the-elation` and `the-remembrance`.
- Confirm USW-Aggregation management IP after UniFi setup.
- Confirm whether AT&T router LAN port negotiates at 1G or higher.
- Confirm physical node hardware models, CPU, memory, disk, and NIC interface names.
- Confirm whether `talos-worker-01` and `talos-worker-02` should use `192.168.1.179` and `192.168.1.180`.
