# IP Plan

This file tracks home lab subnets, reserved addresses, active assignments, and planned addresses.

## Networks

| Network | CIDR | Purpose | Notes |
| --- | --- | --- | --- |
| Physical LAN | `192.168.1.0/24` | Home LAN and lab management | Current flat network behind AT&T router |
| Harvester pod CIDR | `10.52.0.0/16` | Harvester internal pods | Separate from Talos/Kubernetes pod CIDR |
| Harvester service CIDR | `10.53.0.0/16` | Harvester internal services | Separate from Talos/Kubernetes service CIDR |
| Talos pod CIDR | `10.42.0.0/16` | Kubernetes pods | Used by `homelab-talos` |
| Talos service CIDR | `10.43.0.0/16` | Kubernetes services | Used by `homelab-talos` |

## Active IP Assignments

| IP | Name | Role | Status | Notes |
| --- | --- | --- | --- | --- |
| `192.168.1.254` | `att-router` | Router / gateway | active | Default gateway |
| `192.168.1.241` | `the-abundance` | Harvester physical node | active | Current known node IP |
| `192.168.1.50` | `harvester-vip` | Harvester VIP/UI | active | Shared Harvester access IP |
| `192.168.1.178` | `talos-cp-01` | Talos control-plane VM | active | Kubernetes API endpoint host |

## Planned / Reserved IPs

| IP | Name | Role | Status | Notes |
| --- | --- | --- | --- | --- |
| `TBD` | `usw-aggregation` | UniFi switch management | planned | Set during UniFi adoption |
| `TBD` | `the-elation` | Harvester physical node | planned | Required for node monitoring and management |
| `TBD` | `the-remembrance` | Harvester physical node | planned | Required for node monitoring and management |
| `192.168.1.179` | `talos-worker-01` | Talos worker VM | proposed | Confirm before assigning |
| `192.168.1.180` | `talos-worker-02` | Talos worker VM | proposed | Confirm before assigning |

## Allocation Notes

- Harvester VIP/UI is shared, but each physical Harvester node should still have a unique management IP.
- Keep Talos VM IPs near the control-plane IP if available: `192.168.1.178-180`.
- Avoid assigning Harvester, Talos, switch, or monitoring addresses from an unmanaged DHCP pool without reservations.
