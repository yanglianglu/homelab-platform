# Data Platform

This domain owns Kubernetes workloads that intentionally run on the tainted
`data-01` Talos worker.

Initial boundaries:

- Namespace: `data-platform`
- AppProject: `data-platform`
- Node selector: `homelab.local/node-class=data`
- Toleration: `data-platform=true:NoSchedule`
- Retained data: CSI PVC using `harvester-slow-retain`
- Hot/temp data: CSI PVC using `harvester-abundance-nvme-delete`

Do not create production ClickHouse ingestion until node metrics, disk metrics,
and basic alerts are in place.

`data-01` is the scheduling anchor, not the first-choice owner of manually
mounted local PVs. Static local PVs are a fallback only if Harvester CSI is
rejected after proof and the fallback is explicitly approved.

Current status: the small Harvester CSI proof passes on `data-01` after the
`harvester-csi-mountpoint` Talos extension. This validates disposable proof PVC
cleanup on that node.

Keep ClickHouse production ingestion blocked until larger CSI reboot,
maintenance, expansion, and performance drills pass.
