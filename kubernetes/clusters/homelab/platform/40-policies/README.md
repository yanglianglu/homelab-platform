# Policies

Policy guardrails live here.

This component is reconciled by the `platform-policies` Argo CD Application at
sync wave `40`.

Start with built-in Kubernetes controls:

- Pod Security Admission namespace labels.
- ValidatingAdmissionPolicy later for simple CEL-based rules.

Consider Kyverno or Gatekeeper only after built-in controls are not enough.

The current `kustomization.yaml` is intentionally empty. Add ResourceQuota,
LimitRange, NetworkPolicy, or admission policies here only after reviewing their
blast radius against existing workloads.
