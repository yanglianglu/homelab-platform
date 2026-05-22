# whoami-tls

First internal HTTPS route for FIF-21.

- Hostname: `whoami.home.arpa`
- Gateway VIP: `192.168.1.187`
- Gateway: `apps/internal-https`
- Client to Gateway: HTTPS terminated by Envoy Gateway
- Gateway to backend: HTTPS with `BackendTLSPolicy` certificate validation
- Certificate source: `homelab-internal-ca` cert-manager ClusterIssuer
- Trust source: `homelab-internal-ca` trust-manager ConfigMap in `apps`

This app intentionally avoids public DNS, Cloudflare, legacy Ingress, and
plaintext backend traffic.

## Verification

Cluster-side verification can use a temporary curl pod that mounts the
`homelab-internal-ca` trust-manager ConfigMap as `/trust/ca.crt`.

Expected checks:

- `Certificate/whoami-home-arpa-gateway` is Ready.
- `Certificate/whoami-tls-backend` is Ready.
- `Gateway/internal-https` is Accepted and Programmed.
- `HTTPRoute/whoami-tls` is Accepted and ResolvedRefs=True.
- `BackendTLSPolicy/whoami-tls` is Accepted and ResolvedRefs=True.
- Direct backend curl with `--cacert /trust/ca.crt` returns
  `homelab internal HTTPS backend`.
- Gateway curl with `--resolve whoami.home.arpa:443:192.168.1.187` and
  `--cacert /trust/ca.crt` returns `homelab internal HTTPS backend`.
- Normal client curl from the admin Mac works without `--resolve` or
  `--insecure`.

Client closeout is complete for the admin Mac:
`whoami.home.arpa -> 192.168.1.187` resolves locally and the internal CA is
trusted. Additional client machines or browsers must still receive equivalent
DNS and CA trust before they can browse the route without warnings.
