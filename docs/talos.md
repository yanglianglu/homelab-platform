# Talos

Talos turns the Harvester VMs into Kubernetes nodes. The source files for the `homelab-talos` cluster live under `talos/clusters/homelab`.

## Current Cluster

| Item | Value |
| --- | --- |
| Cluster name | `homelab-talos` |
| Control-plane endpoint | `https://192.168.1.178:6443` |
| Node | `talos-cp-01` |
| Node IP | `192.168.1.178` |
| Talos version | `v1.13.0` |
| Install disk | `/dev/vda` |
| Pod CIDR | `10.42.0.0/16` |
| Service CIDR | `10.43.0.0/16` |
| Bootstrap status | Completed |
| Health status | Completed successfully |

## Milestone

The first control-plane node, `talos-cp-01`, is bootstrapped and healthy. Talos API checks, service/address/route inspection, Kubernetes bootstrap, kubeconfig generation, and core pod checks have completed.

## Secret Handling

Generated files such as `controlplane.yaml`, `worker.yaml`, `talosconfig`, `secrets.yaml`, and kubeconfig can contain sensitive material. Keep them local unless they are encrypted with a tool such as SOPS and age.
