# Port Map

This file tracks physical switch port connections. Update it whenever cabling changes.

## USW-Aggregation

| Switch Port | Connected Device | Connected Interface | Speed Target | Cable / Adapter | Network | Status | Notes |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| `sfp1` | `the-abundance` | `TBD` | 10G | DAC | LAN / Harvester `mgmt` / `lan-untagged` | planned | SFP+ node |
| `sfp2` | `the-elation` | `TBD` | 10G | DAC | LAN / Harvester `mgmt` / `lan-untagged` | planned | SFP+ node |
| `sfp3` | `the-enigmata` | `TBD` | 1G | SFP-to-RJ45 module | LAN / Harvester `mgmt` / `lan-untagged` | planned | RJ45 node on SFP+ switch |
| `sfp4` | unused | - | - | - | - | open | Available |
| `sfp5` | unused | - | - | - | - | open | Available |
| `sfp6` | unused | - | - | - | - | open | Available |
| `sfp7` | unused | - | - | - | - | open | Available |
| `sfp8` | `att-router` | LAN port | likely 1G | SFP-to-RJ45 module | Physical LAN | planned | Current router uplink |

## Notes

- USW-Aggregation ports are SFP+ cages. RJ45 devices need compatible SFP/SFP+ RJ45 transceiver modules.
- DAC cables are appropriate for direct SFP+ to SFP+ links, such as `the-abundance` and `the-elation`.
- `the-enigmata` is the verified third Harvester node. Older `the-remembrance` references are stale unless that host is reintroduced later.
- The third node is expected to run at 1G unless its NIC is upgraded.
- No firewall is planned yet, so the AT&T router remains the gateway.
