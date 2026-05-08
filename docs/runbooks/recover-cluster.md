# Runbook: Recover Cluster

Recovery steps belong here as the lab matures. Keep this document practical and incident-focused.

## Initial Checks

1. Confirm Harvester UI is reachable at `192.168.1.50`.
2. Confirm the Harvester node is reachable at `192.168.1.241`.
3. Confirm the Talos node responds at `192.168.1.178`.
4. Check VM power state in Harvester.
5. Check Talos health from a trusted local workstation.

## Do Not

- Do not commit recovered plaintext kubeconfig or Talos secrets.
- Do not replace desired-state files with live exports containing runtime metadata.
