# data-01 Local PVs

Local PV manifests are created only after `data-01` is joined and Talos confirms
the retained and hot/temp disks are mounted at the expected paths.

Current Talos disk map:

| Guest disk | Size | Harvester PVC | Intended path |
| --- | ---: | --- | --- |
| `/dev/vdb` | 10 TiB | `data-01-retained-data` | `/var/mnt/clickhouse-data` |
| `/dev/vdc` | 1 TiB | `data-01-hot-temp` | `/var/mnt/clickhouse-hot` |

Expected paths:

- `/var/mnt/clickhouse-data`
- `/var/mnt/clickhouse-hot`

Stop if those paths are not backed by the expected Harvester disks.
