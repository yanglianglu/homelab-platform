# Generated Talos Files

This directory is intentionally not used for committed generated Talos secrets.

Do not commit plaintext generated files such as:

- controlplane.yaml
- worker.yaml
- talosconfig
- kubeconfig
- secrets.yaml

These files contain cluster credentials, certificates, and tokens.

For now, store generated files locally outside Git, for example:

`C:\homelab-secrets\talos-homelab\`

Future option: encrypt generated secrets with SOPS + age before committing.
