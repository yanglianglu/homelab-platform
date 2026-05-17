# Kubelet CSR Approver

This Argo CD Application installs `postfinance/kubelet-csr-approver` so Talos
kubelets can receive signed serving certificates after
`serverTLSBootstrap: true` is enabled.

The approver only approves kubelet-serving CSRs that match the expected homelab
node identity and LAN constraints:

- Signer: `kubernetes.io/kubelet-serving`
- Nodes: `cp-01`, `cp-02`, `cp-03`, `worker-01`, `worker-02`, `data-01`
- Node username/common name shape: `system:node:<node-name>`
- IP SAN range: `192.168.1.0/24`
- DNS SAN count: at most one
- Max requested expiration: `31536000` seconds

`bypassDnsResolution` is enabled because the short Talos node names are not
treated as a cluster DNS contract. The node-name regex, kubelet-serving signer,
`system:node:` identity checks, and LAN IP prefix remain enforced.

The approver is configured with `skipDenyStep: true`, so questionable CSRs are
ignored instead of denied. This keeps the first hardening gate reversible while
still preventing automatic approval of CSRs outside the constraints.

## Verification

```bash
kubectl --context homelab-talos -n argocd get application platform-kubelet-csr-approver
kubectl --context homelab-talos -n kube-system get pods -l app.kubernetes.io/name=kubelet-csr-approver
kubectl --context homelab-talos get csr
```

Approved kubelet serving CSRs should use signer
`kubernetes.io/kubelet-serving`, requestor `system:node:<node-name>`, and show
`Approved,Issued` only for the six expected nodes.

## Rollback

If the approver behaves unexpectedly, remove or disable this Application before
continuing Talos rollout. Do not remove Metrics Server
`--kubelet-insecure-tls` until all six expected kubelet-serving CSRs are
`Approved,Issued` and the CSR contents match the expected node names and
`192.168.1.0/24` addresses.
