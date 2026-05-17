# Runbook: Admin Access Pattern

This runbook defines the initial private/admin access model for the homelab.

It is a decision and operating contract, not a completed VPN installation
record. Add implementation commands here when the first Tailscale subnet router
is created.

## Decision

Use Tailscale as the first remote admin VPN path.

The initial goal is private administration without exposing homelab management
interfaces to the public internet.

## Compared Options

| Option | Decision | Why |
| --- | --- | --- |
| Existing LAN only | Keep for local use | Fine at home, but not a remote admin pattern |
| Tailscale | Choose first | Fast setup, no inbound router ports, device identity, subnet routing path |
| Raw WireGuard | Defer | More manual key/routing work before the platform baseline is stable |
| Cloudflare Tunnel | Not for admin baseline | Deferred until after the internal-only Gateway API route is proven |

## Initial Target Shape

```text
Admin laptop / trusted device
  -> Tailscale tailnet
  -> future subnet router on homelab LAN
  -> private homelab admin surfaces
```

The future subnet router should be a small, dedicated LAN-attached system or VM.
Do not run it as the first workload inside the guest Kubernetes cluster; the VPN
path should remain available even if the guest cluster is unhealthy.

## Admin-Only Surfaces

Keep these private:

| Surface | Address / Access | Notes |
| --- | --- | --- |
| Harvester UI/API | `192.168.1.50` | Harvester VIP |
| Harvester nodes | `192.168.1.241`, `192.168.1.250`, `192.168.1.244` | Node-level management |
| Talos control plane | `192.168.1.181` | `talosctl` and Kubernetes API endpoint host |
| Kubernetes API | context `homelab-talos` | Use kubeconfig, never public Gateway or Ingress |
| Argo CD | port-forward first | Do not expose until identity-aware access exists |
| Router/switch/DNS | LAN-only addresses | Keep management private |
| Observability/admin dashboards | TBD | Require identity-aware access before exposure |

## Guardrails

- Do not open random inbound ports on the AT&T router for admin access.
- Do not expose Harvester, Talos, Kubernetes API, or Argo CD directly through
  public Gateway routes or legacy Ingress.
- Do not store Tailscale auth keys, WireGuard private keys, kubeconfigs, or
  admin credentials in Git.
- Prefer device/user identity and least privilege over shared long-lived secrets.
- Keep public app exposure separate from private admin access.
- Document any subnet routes, advertised CIDRs, and approved admin devices when
  implementation starts.

## Future Implementation Checklist

1. Choose the subnet-router host or VM.
2. Install Tailscale on the subnet-router host.
3. Advertise only the needed private routes at first, likely `192.168.1.0/24`.
4. Approve the subnet route in the Tailscale admin console.
5. Restrict tailnet access to trusted admin identities/devices.
6. Verify access to:
   - Harvester VIP `192.168.1.50`
   - Talos API host `192.168.1.181`
   - Kubernetes context `homelab-talos`
7. Confirm public app exposure still does not depend on this admin VPN.
8. Update `docs/network.md`, `docs/network-inventory.md`, and `docs/ip-plan.md`
   with the chosen subnet-router host and address.

## Verification Commands

Use these after implementation, not before:

```bash
tailscale status
tailscale ping <subnet-router-name>
kubectl --context homelab-talos get nodes -o wide
talosctl --nodes 192.168.1.181 health
```

For Argo CD, continue to prefer local-only access until identity-aware access is
implemented:

```bash
kubectl --context homelab-talos -n argocd port-forward svc/argocd-server 8080:443
```

## Follow-Ups

- Define the internal DNS and Gateway address model.
- Install Gateway API, Envoy Gateway, cert-manager, and trust-manager for the
  first internal HTTPS route.
- Protect the first dashboard or test app with identity-aware access.
