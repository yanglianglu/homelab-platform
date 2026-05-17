# Observability Domain

This directory owns observability services inside the `homelab-talos` guest cluster.

Harvester-level monitoring is separate and already enabled through the
Harvester `rancher-monitoring` addon in `cattle-monitoring-system`. Do not
duplicate Harvester host, VM, and Longhorn collection here unless a later
datasource integration is explicitly planned.

Examples:

- VictoriaMetrics
- Grafana
- exporters
- alerting

Start with small resource requests and grow based on real scrape volume, retention, dashboard usage, and alerting needs.

See `docs/architecture/observability-plan.md` for the Harvester versus guest
Kubernetes observability boundary.
