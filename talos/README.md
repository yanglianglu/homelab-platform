# Talos

`talos/` stores Talos source configuration, patches, and scripts for the `homelab-talos` cluster.

It does not store plaintext generated Talos configs. Generated files should be kept outside Git or encrypted with SOPS later.

Current control-plane endpoint:

- `https://192.168.1.178:6443`

## Safe Source Files

Safe files to commit here:

- Cluster variables
- Talos patches
- Helper scripts
- Documentation and runbooks

Do not commit plaintext generated files such as `controlplane.yaml`, `worker.yaml`, `talosconfig`, `kubeconfig`, or `secrets.yaml`.
