# Runbook: Repair cp-01 ISO Boot

Use this when Harvester reports `cp-01` as Running/Ready, but the Talos node at
`192.168.1.181` is unreachable and the VM appears to have booted the Talos ISO
instead of the installed OS disk.

Do not treat IPv6-only VMI output as a failure by itself. Current healthy VMIs
can show IPv6 addresses in Harvester while their Talos nodes are Ready on the
expected IPv4 addresses inside `homelab-talos`.

## Symptom

- `cp-01` VMI is Running and Ready in Harvester.
- `192.168.1.181` does not answer ARP or ping.
- `192.168.1.181:6443` is unreachable.
- Harvester VMI status plus LAN checks suggest the expected IPv4 path is absent.
- TCP ports `50000` and `6443` are refused on that IPv6 address.

## Likely Cause

The VM restarted while the Talos ISO was still boot order 1. The VM can boot into
the ISO/live environment instead of the installed Talos OS disk. In that state,
the guest may be alive on the LAN but not running the configured control plane.

## Read-Only Confirmation

```bash
kubectl --context harvester -n talos-cluster get vm cp-01 \
  -o jsonpath='{range .spec.template.spec.domain.devices.disks[*]}name={.name}{"\n"}bootOrder={.bootOrder}{"\n"}{end}'

kubectl --context harvester -n talos-cluster get vmi cp-01 \
  -o 'custom-columns=NAME:.metadata.name,PHASE:.status.phase,NODE:.status.nodeName,IP:.status.interfaces[*].ipAddress,MAC:.status.interfaces[*].mac'
```

If `talos-iso` is boot order 1 and `os-disk` is boot order 2, repair the boot
order before adding more Talos nodes.

## Repair Decision

The live VM repair is a deliberate mutating operation:

1. Update `cp-01` so the OS disk is the first boot device.
2. Detach the Talos ISO from the VM template or ensure it cannot boot before the OS disk.
3. Restart `cp-01`.
4. Confirm `192.168.1.181` returns.
5. Confirm Talos and Kubernetes APIs are reachable.

Do not rely on `cp-01` as a healthy control-plane endpoint until this repair
gate passes. In the current HA cluster, use the kube-vip endpoint and the other
control-plane nodes for normal API access while investigating `cp-01`.
