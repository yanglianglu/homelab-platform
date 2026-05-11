# Network

Human-readable network notes for the home lab. This file documents intended addressing and CIDR boundaries; deployment manifests live outside `docs/`.

| Network Item | Value |
| --- | --- |
| Physical LAN | `192.168.1.0/24` |
| Router/Gateway | `192.168.1.254` |
| Harvester node IPs | `192.168.1.241` (`the-abundance`), `192.168.1.250` (`the-elation`), `192.168.1.244` (`the-enigmata`) |
| Harvester VIP/UI | `192.168.1.50` |
| Switching | `USW-Aggregation` planned/current setup in progress |
| Harvester pod CIDR | `10.52.0.0/16` |
| Harvester service CIDR | `10.53.0.0/16` |
| Harvester Cluster Network | `mgmt` |
| Harvester VM Network | `lan-untagged` |
| Talos control-plane IP | `192.168.1.181` (`cp-01`) |
| Talos pod CIDR | `10.42.0.0/16` |
| Talos service CIDR | `10.43.0.0/16` |

## Notes

- Current network path is `AT&T Router -> USW-Aggregation -> physical Harvester nodes`. No dedicated firewall is planned yet.
- Harvester VIP/UI `192.168.1.50` is the shared UI/API access point. Each physical Harvester node has its own management IP for node-level operations and monitoring.
- Cluster Network `mgmt` is the Harvester L2/uplink path.
- VM Network `lan-untagged` is the Multus-backed VM attachment network used by Talos VMs.
- Harvester and Talos use separate pod and service CIDRs.
- Overlapping CIDRs can be technically possible when networks are isolated, but they are not recommended because troubleshooting and routing become harder.
- Talos VM traffic is expected to land on the physical LAN through the Harvester `lan-untagged` VM network.
- Old `talos-cp-01` remains at `192.168.1.178` until retirement.
- Keep router/DHCP reservations and static IP decisions documented here.

## Inventory Files

- `docs/network-inventory.md` tracks devices, roles, management IPs, and status.
- `docs/ip-plan.md` tracks subnets, reserved addresses, and planned node IPs.
- `docs/port-map.md` tracks USW-Aggregation port connections.
- `docs/network-map.md` tracks the current logical topology.
