# kube-vip

`kube-vip` advertises LAN-only virtual IPs for `homelab-talos`.

## Control Plane VIP

The `kube-vip` DaemonSet advertises the internal Kubernetes API VIP
`192.168.1.184` on the LAN. It runs only on control-plane nodes in
`kube-system`.

This is cluster plumbing, not public exposure. Keep individual control-plane IPs
available for break-glass access.

## Service LoadBalancer VIPs

The `kube-vip-service-lb` DaemonSet enables kube-vip Service LoadBalancer mode
on the general worker nodes only. It is intended for internal LoadBalancer
Services such as the future Envoy Gateway Service.

Initial planned VIP:

| IP | Intended owner | Notes |
| --- | --- | --- |
| `192.168.1.187` | internal Envoy Gateway | `192.168.1.186` responded to ping; reserve `.187` in LAN/DHCP before Gateway Service sync |

Guardrails:

- keep this internal-only
- do not use it for Harvester, Talos, Kubernetes API, or Argo CD admin exposure
- verify the VIP is reserved and unused before live sync
- require an explicit live gate before syncing this change
