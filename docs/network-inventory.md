# Network Inventory

This file is the lightweight source of truth for current and planned home lab network devices. It is intentionally simple enough to maintain in Git before adding a heavier inventory tool such as NetBox.

## Current Topology

```text
Internet
  -> AT&T Router
  -> USW-Aggregation
      -> the-abundance
      -> the-elation
      -> the-enigmata
```

No dedicated firewall is planned at this stage. The AT&T router remains the gateway.

## Devices

| Device | Role | Management IP | Platform / Model | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `att-router` | Router / gateway | `192.168.1.254` | AT&T Fiber Router | active | Current default gateway |
| `usw-aggregation` | 10G aggregation switch | `TBD` | UniFi USW-Aggregation | not set up | Connected directly to AT&T router |
| `the-abundance` | Physical Harvester node | `192.168.1.241` | TBD | active | Hosts current Harvester environment and `cp-01` |
| `the-elation` | Physical Harvester node | `192.168.1.250` | TBD | active | Verified Ready in Harvester |
| `the-enigmata` | Physical Harvester node | `192.168.1.244` | TBD | active | Verified Ready in Harvester |
| `harvester-vip` | Harvester UI/API VIP | `192.168.1.50` | Harvester VIP | active | Shared Harvester access IP |
| `cp-01` | Talos control-plane VM | `192.168.1.181` | Talos v1.13.0 | active | Fresh replacement control plane; bootstrapped and healthy |
| `worker-01` | Talos worker VM | `192.168.1.179` | Talos v1.13.0 | active | General worker VM on `the-elation` |
| `worker-02` | Talos worker VM | `192.168.1.180` | Talos v1.13.0 | active | General worker VM on `the-enigmata` |
| `cp-02` | Talos control-plane VM | `192.168.1.182` | Talos v1.13.0 | active | Control-plane VM on `the-elation` |
| `cp-03` | Talos control-plane VM | `192.168.1.183` | Talos v1.13.0 | active | Control-plane VM on `the-enigmata` |
| `homelab-talos-api` | Kubernetes API VIP | `192.168.1.184` | n/a | active | Stable kube-vip API endpoint |

## Node Link Plan

| Node | Link Type | Target Speed | Switch Port | Cable / Adapter | Notes |
| --- | --- | ---: | --- | --- | --- |
| `the-abundance` | SFP+ | 10G | `sfp1` | DAC | Direct SFP+ preferred |
| `the-elation` | SFP+ | 10G | `sfp2` | DAC | Direct SFP+ preferred |
| `the-enigmata` | RJ45 | 1G | `sfp3` | SFP-to-RJ45 module | USW-Aggregation is SFP+, so RJ45 requires a transceiver/module |
| `att-router` | RJ45 | likely 1G | `sfp8` | SFP-to-RJ45 module | Uplink to current gateway |

## Open Items

- Confirm USW-Aggregation management IP after UniFi setup.
- Confirm whether AT&T router LAN port negotiates at 1G or higher.
- Confirm physical node hardware models, CPU, memory, disk, and NIC interface names.
- Confirm final MAC addresses when `worker-01` and `worker-02` are created.
- Confirm whether the `the-enigmata` link should remain 1G or be upgraded later.
- Confirm whether retired IP `192.168.1.178` is released or reserved before reuse.
