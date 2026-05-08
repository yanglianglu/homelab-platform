# Runbook: Apply Talos Config

Use this after the `talos-cp-01` VM exists and is booted from the Talos ISO.

## Local Steps

This is the exact sequence used for the first control-plane node:

```powershell
cd C:\Users\91725\OneDrive\Documents

talosctl get disks --insecure --nodes 192.168.1.178

talosctl gen config homelab-talos https://192.168.1.178:6443 `
  --install-disk /dev/vda `
  --config-patch "@.\cluster-network.yaml" `
  --force

Select-String -Path .\controlplane.yaml -Pattern "10.42.0.0|10.43.0.0"

talosctl validate --config .\controlplane.yaml --mode metal --strict

talosctl apply-config --insecure `
  --nodes 192.168.1.178 `
  --file .\controlplane.yaml

$env:TALOSCONFIG = (Resolve-Path .\talosconfig).Path
talosctl config endpoint 192.168.1.178
talosctl config node 192.168.1.178

talosctl version
talosctl get services
talosctl get addresses
talosctl get routes

talosctl bootstrap
talosctl kubeconfig .

kubectl --kubeconfig .\kubeconfig get pods -A -o wide
talosctl health
```

## Notes

- `talosctl bootstrap` should only be run once for the first control-plane node.
- Do not regenerate configs with new PKI after the cluster is active unless intentionally rebuilding the cluster.
- Do not commit plaintext generated secrets, `talosconfig`, `controlplane.yaml`, `worker.yaml`, `secrets.yaml`, or kubeconfig.
- Review generated files before applying.
- The repository scripts under `talos/clusters/homelab/scripts/` keep the same workflow in a safer repeatable location.
