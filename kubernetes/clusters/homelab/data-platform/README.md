# Data Platform

This domain owns Kubernetes workloads that intentionally run on the tainted
`data-01` Talos worker.

Initial boundaries:

- Namespace: `data-platform`
- AppProject: `data-platform`
- Node selector: `homelab.local/node-class=data`
- Toleration: `data-platform=true:NoSchedule`
- Retained data disk: Harvester `slow` storage attached to `data-01`
- Hot/temp disk: Harvester `the-abundance-nvme` storage attached to `data-01`

Do not create production ClickHouse ingestion until node metrics, disk metrics,
and basic alerts are in place.
