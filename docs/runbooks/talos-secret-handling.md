# Runbook: Talos Secret Handling

Generated Talos files contain sensitive credentials, certificates, and tokens.

Do not commit plaintext generated files such as:

- `controlplane.yaml`
- `worker.yaml`
- `talosconfig`
- `kubeconfig`
- `secrets.yaml`
- private keys, certificates, or tokens

For now, store generated files locally outside Git:

`C:\homelab-secrets\talos-homelab\`

On macOS, use an equivalent local-only path such as:

```text
~/.local/share/homelab-secrets/talos-homelab/
```

Keep at least these files if the existing cluster should remain recoverable:

- `talosconfig`
- `secrets.yaml`
- `kubeconfig`

Do not regenerate a new Talos config for an already-bootstrapped node unless intentionally rebuilding the cluster. New generated secrets create a different PKI and will not authenticate to the existing node.

Future option: use SOPS + age to encrypt generated secrets before committing.

If generated configs are accidentally committed, treat them as exposed. Depending on where they were pushed and who could access them, rotate credentials or rebuild the cluster PKI. For a small lab, a deliberate rebuild may be simpler than partial rotation.
