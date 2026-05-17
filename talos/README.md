# Talos

`talos/` stores Talos source configuration, patches, and scripts for the `homelab-talos` cluster.

It does not store plaintext generated Talos configs. Generated files should be kept outside Git or encrypted with SOPS later.

Current control-plane endpoint:

- `https://192.168.1.184:6443`

## Safe Source Files

Safe files to commit here:

- Cluster variables
- Talos patches
- Helper scripts
- Documentation and runbooks

Do not commit plaintext generated files such as `controlplane.yaml`, `worker.yaml`, `talosconfig`, `kubeconfig`, or `secrets.yaml`.

## macOS Helper Scripts

Run helper scripts from `talos/clusters/homelab`:

```bash
scripts/render.sh
scripts/validate.sh
scripts/apply-controlplane.sh
scripts/dry-run.sh
scripts/bootstrap.sh
```

`bootstrap.sh` should only be used once for the first control-plane bootstrap.

## Recovery Strategy

The current recovery preference is rebuild first, snapshot only for short-term rollback, and VM backup only after a Harvester backup target exists.

`cp-01`, `cp-02`, and `cp-03` are the active control-plane nodes. The old
`talos-cp-01` VM has been retired, so do not add desired state for it back to
Git unless a future recovery plan explicitly needs a historical reference.

See `docs/runbooks/talos-vm-recovery-strategy.md`.
