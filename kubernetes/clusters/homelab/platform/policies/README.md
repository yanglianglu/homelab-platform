# Policies

Policy guardrails live here.

Start with built-in Kubernetes controls:

- Pod Security Admission namespace labels.
- ValidatingAdmissionPolicy later for simple CEL-based rules.

Consider Kyverno or Gatekeeper only after built-in controls are not enough.
