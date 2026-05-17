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
| Talos API VIP | `192.168.1.184` (`homelab-talos-api`) |
| Talos control-plane IPs | `192.168.1.181` (`cp-01`), `192.168.1.182` (`cp-02`), `192.168.1.183` (`cp-03`) |
| Talos pod CIDR | `10.42.0.0/16` |
| Talos service CIDR | `10.43.0.0/16` |
| Internal Gateway VIP | `192.168.1.187` (`homelab-gateway-vip`) |
| First internal Gateway hostname | `whoami.home.arpa` |

## Admin Access Pattern

Initial decision: use **Tailscale as the first admin VPN path** for remote
homelab administration.

Rationale:

- It does not require opening inbound ports on the AT&T router.
- It separates private/admin access from future public app exposure.
- It is faster to operate safely than hand-managed WireGuard while the platform
  baseline is still changing.
- It can support a dedicated subnet router later so approved admin devices can
  reach private LAN addresses such as Harvester, Talos, and Kubernetes.

Deferred alternatives:

- Raw WireGuard is a reasonable future option if self-hosted VPN control becomes
  more important than operational speed.
- Cloudflare Tunnel is deferred. The first secure app route should be
  internal-only Gateway API, not public exposure.
- Existing LAN-only access remains valid when physically at home, but it is not
  the remote admin access pattern.

Admin-only surfaces include:

- Harvester VIP/UI and physical node management IPs
- Talos API and `talosctl` access
- Guest Kubernetes API and `kubectl` access
- Argo CD UI/API access, still local-only through port-forward until a stronger
  identity-aware access layer exists
- Router, switch, DNS, and future observability/admin dashboards

Do not expose admin surfaces through public Gateway routes, legacy Ingress, or
Cloudflare Tunnel as part of Stage 4. Public app exposure and identity-aware app
protection are separate follow-up decisions.

Operational details live in `docs/runbooks/admin-access.md`.

## Internal Gateway API Track

The first HTTPS application route is internal-only:

- Gateway API, implemented by Envoy Gateway
- cert-manager for Gateway and backend certificates
- trust-manager for internal CA bundle distribution
- internal CA first, not public ACME
- internal DNS only; `whoami.home.arpa` must resolve to `192.168.1.187`
- HTTPS from client to Gateway
- HTTPS from Gateway to backend, verified with `BackendTLSPolicy`

No Cloudflare Tunnel, NGINX Ingress, public DNS, public ACME, service mesh, or
plaintext backend is part of the first route.

The durable implementation plan lives in
`docs/architecture/internal-gateway-api-plan.md`.

Current state: the first route is live in Kubernetes and the VIP is advertised
by kube-vip. The remaining client-facing task is to add internal DNS for
`whoami.home.arpa` and install/trust the internal CA on client machines that
should browse the route without warnings.

## Notes

- Current network path is `AT&T Router -> USW-Aggregation -> physical Harvester nodes`. No dedicated firewall is planned yet.
- Harvester VIP/UI `192.168.1.50` is the shared UI/API access point. Each physical Harvester node has its own management IP for node-level operations and monitoring.
- Cluster Network `mgmt` is the Harvester L2/uplink path.
- VM Network `lan-untagged` is the Multus-backed VM attachment network used by Talos VMs.
- Harvester and Talos use separate pod and service CIDRs.
- Overlapping CIDRs can be technically possible when networks are isolated, but they are not recommended because troubleshooting and routing become harder.
- Talos VM traffic is expected to land on the physical LAN through the Harvester `lan-untagged` VM network.
- Old `talos-cp-01` at `192.168.1.178` has been retired. Reuse that IP only after checking DHCP/reservation state.
- Keep router/DHCP reservations and static IP decisions documented here.

## Inventory Files

- `docs/network-inventory.md` tracks devices, roles, management IPs, and status.
- `docs/ip-plan.md` tracks subnets, reserved addresses, and planned node IPs.
- `docs/port-map.md` tracks USW-Aggregation port connections.
- `docs/network-map.md` tracks the current logical topology.
- `docs/runbooks/admin-access.md` tracks the admin VPN access pattern.
