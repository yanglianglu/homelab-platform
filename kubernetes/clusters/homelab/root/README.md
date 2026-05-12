# Root

The cluster root is `kubernetes/clusters/homelab/kustomization.yaml`.

The original design considered placing the root kustomization in this
directory and referencing sibling directories with `../projects` and
`../platform/...`. Default Kustomize rejects that pattern because resources
outside the kustomization root require a relaxed load restrictor.

Keeping the root at `kubernetes/clusters/homelab/` lets Argo CD and local
validation use the default Kustomize security model while still keeping
AppProjects and child Applications organized by platform capability.
