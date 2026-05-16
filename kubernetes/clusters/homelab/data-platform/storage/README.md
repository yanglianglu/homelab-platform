# data-01 Local PVs

Local PV manifests are created only after `data-01` is joined and Talos confirms
the retained and hot/temp disks are mounted at the expected paths.

Expected paths:

- `/var/mnt/clickhouse-data`
- `/var/mnt/clickhouse-hot`

Stop if those paths are not backed by the expected Harvester disks.
