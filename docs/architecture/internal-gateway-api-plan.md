# Internal Gateway API Plan

This plan replaces the older Stage 4 exposure wording with an internal-only
Gateway API track.

## Target

The first secure route should prove an internal HTTPS hostname can reach a test
service with encrypted and verified traffic on both hops:

```text
internal client -> Envoy Gateway -> HTTPS backend service
```

## Decisions

| Area | Decision |
| --- | --- |
| External provider | None for the first route |
| Cloudflare | Excluded from this issue |
| Legacy Ingress / NGINX | Excluded from this issue |
| Routing API | Gateway API |
| Gateway implementation | Envoy Gateway |
| Gateway address model | kube-vip Service LoadBalancer VIP |
| Initial Gateway VIP | `192.168.1.187`, advertised by kube-vip |
| First hostname | `whoami.home.arpa` |
| Client to Gateway | HTTPS |
| Gateway to backend service | HTTPS with certificate verification |
| Backend TLS policy | `BackendTLSPolicy` |
| Certificate manager | One cert-manager installation |
| Trust distribution | trust-manager |
| Certificate source | Internal CA first |
| DNS | Internal-only hostname and address |
| Deployment model | Argo CD / GitOps |
| Service mesh | Excluded for this issue |

## Current State

The Gateway, certificates, trust bundle, HTTPS backend, `HTTPRoute`, and
`BackendTLSPolicy` are live through Argo CD.

Verified live state:

- `apps-whoami-tls` is Synced and Healthy.
- `Gateway/apps/internal-https` is Accepted and Programmed on
  `192.168.1.187`.
- Envoy Gateway created a LoadBalancer Service with
  `kube-vip.io/loadbalancerIPs: 192.168.1.187`.
- kube-vip advertises `192.168.1.187` for the generated Envoy Service.
- `Certificate/whoami-home-arpa-gateway` and
  `Certificate/whoami-tls-backend` are Ready.
- `HTTPRoute/apps/whoami-tls` is Accepted and ResolvedRefs=True.
- `BackendTLSPolicy/apps/whoami-tls` is Accepted and ResolvedRefs=True.
- A trusted curl test through the Gateway returns the HTTPS backend response.

Remaining before Linear closeout:

- Add internal DNS for `whoami.home.arpa -> 192.168.1.187`.
- Install or otherwise trust the internal CA on client machines that should
  browse the route without certificate warnings.

## Scope

FIF-21 is now interpreted as:

```text
Install Gateway API, cert-manager, trust-manager, and the first internal HTTPS route.
```

The issue still owns the first user-visible proof: an internal hostname reaches
a test app over HTTPS, the Gateway presents an internally trusted certificate,
the backend service presents its own certificate, and the Gateway verifies the
backend certificate before forwarding traffic.

## Implementation Gates

1. Confirm guest observability is usable for Gateway, cert-manager,
   trust-manager, route, and backend debugging.
2. Enable kube-vip Service LoadBalancer mode on general workers for the internal
   Gateway VIP.
3. Install Gateway API CRDs through GitOps using `platform-gateway-api-crds`.
4. Install Envoy Gateway through GitOps using `platform-envoy-gateway`.
5. Create the Envoy-managed `GatewayClass`.
6. Create an internal HTTPS `Gateway` listener only.
7. Install cert-manager with Gateway API support enabled.
8. Create the internal CA issuer model for Gateway and backend certificates.
9. Install trust-manager.
10. Create a trust-manager `Bundle` that writes the internal CA bundle where
   Gateway backend validation needs it.
11. Deploy an HTTPS-capable test backend with a cert-manager-issued service
    certificate.
12. Add an `HTTPRoute` for the internal hostname.
13. Add a same-namespace `BackendTLSPolicy` targeting the backend `Service`.
14. Verify internal DNS and client trust.
15. Document verification, rollback, and the final live state.

## Acceptance Criteria

- kube-vip Service LoadBalancer pods are healthy on general workers.
- Internal Gateway VIP is reserved, assigned, and advertised by kube-vip.
- Envoy Gateway controller and data plane are healthy.
- Gateway API CRDs include the standard resources needed for `Gateway`,
  `HTTPRoute`, and `BackendTLSPolicy`.
- cert-manager is healthy and watches Gateway resources.
- trust-manager is healthy and the CA bundle syncs to required namespaces.
- Gateway listener certificate is issued by the internal CA.
- Backend service certificate is issued by the internal CA.
- `HTTPRoute` is accepted and routes the internal hostname to the test service.
- `BackendTLSPolicy` is accepted and makes Envoy use verified HTTPS upstream.
- Internal DNS resolves the hostname to the internal Gateway address.
- Client trust for the internal CA is documented and applied to the intended
  admin client.
- Rollback order is documented before live sync.

## Rollback Order

1. Remove the test `HTTPRoute`.
2. Remove the `BackendTLSPolicy`.
3. Remove the HTTPS test app.
4. Remove the internal `Gateway` if no other routes use it.
5. Keep or remove cert-manager and trust-manager based on whether other
   certificates or bundles already depend on them.
6. Verify existing cluster apps remain healthy.

## Open Implementation Details

The cluster-side implementation is settled. The remaining open detail is the
client-side DNS and trust path:

- preferred internal DNS owner for `home.arpa`
- whether the first client trust proof should use a local hosts entry, router
  DNS, a dedicated resolver, or a future cluster-hosted DNS service
- whether the internal CA should stay cluster-generated or later move to an
  externally managed/intermediate CA delivered through Infisical and External
  Secrets Operator
