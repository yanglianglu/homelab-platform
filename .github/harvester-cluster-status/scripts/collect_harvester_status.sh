#!/usr/bin/env bash
set -uo pipefail

usage() {
  cat <<'EOF'
Usage: collect_harvester_status.sh [options]

Collect a read-only Harvester/RKE2/KubeVirt/Longhorn status snapshot.

Options:
  --output-dir DIR       Directory for collected outputs (default: ./harvester-status-<timestamp>)
  --context NAME         kubectl context to use
  --kubeconfig FILE      kubeconfig path to use
  --event-tail N         Number of recent events to keep (default: 100)
  --restart-threshold N  Collect targeted logs for pods with restarts >= N (default: 10)
  --no-logs              Skip targeted pod logs/describes
  -h, --help             Show this help

Safety:
  This script uses read-only kubectl calls only. It does not get Secret objects
  and does not run apply/create/delete/edit/patch/replace/exec/cp/port-forward.
EOF
}

OUT_DIR=""
CONTEXT=""
KUBECONFIG_ARG=""
EVENT_TAIL=100
RESTART_THRESHOLD=10
COLLECT_LOGS=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-dir)
      OUT_DIR="${2:-}"
      shift 2
      ;;
    --context)
      CONTEXT="${2:-}"
      shift 2
      ;;
    --kubeconfig)
      KUBECONFIG_ARG="${2:-}"
      shift 2
      ;;
    --event-tail)
      EVENT_TAIL="${2:-100}"
      shift 2
      ;;
    --restart-threshold)
      RESTART_THRESHOLD="${2:-10}"
      shift 2
      ;;
    --no-logs)
      COLLECT_LOGS=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! command -v kubectl >/dev/null 2>&1 && [[ -x /var/lib/rancher/rke2/bin/kubectl ]]; then
  export PATH="$PATH:/var/lib/rancher/rke2/bin"
fi

if ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl not found. Add it to PATH or run on a Harvester/RKE2 node." >&2
  exit 127
fi

if [[ -z "${KUBECONFIG:-}" && -z "$KUBECONFIG_ARG" && -r /etc/rancher/rke2/rke2.yaml ]]; then
  export KUBECONFIG=/etc/rancher/rke2/rke2.yaml
fi

if [[ -z "$OUT_DIR" ]]; then
  OUT_DIR="./harvester-status-$(date +%Y%m%d-%H%M%S)"
fi

mkdir -p "$OUT_DIR"/{auth,cluster,pods,control-plane,harvester,vip,vm,cdi,storage,longhorn,network,logs}
COMMAND_LOG="$OUT_DIR/commands-executed.txt"
: > "$COMMAND_LOG"

KUBECTL=(kubectl)
if [[ -n "$CONTEXT" ]]; then
  KUBECTL+=(--context "$CONTEXT")
fi
if [[ -n "$KUBECONFIG_ARG" ]]; then
  KUBECTL+=(--kubeconfig "$KUBECONFIG_ARG")
fi

record_command() {
  printf 'kubectl' >> "$COMMAND_LOG"
  if [[ -n "$CONTEXT" ]]; then
    printf ' --context %q' "$CONTEXT" >> "$COMMAND_LOG"
  fi
  if [[ -n "$KUBECONFIG_ARG" ]]; then
    printf ' --kubeconfig %q' "$KUBECONFIG_ARG" >> "$COMMAND_LOG"
  fi
  printf ' %q' "$@" >> "$COMMAND_LOG"
  printf '\n' >> "$COMMAND_LOG"
}

run_kubectl() {
  local rel_path="$1"
  shift
  local path="$OUT_DIR/$rel_path"
  mkdir -p "$(dirname "$path")"
  record_command "$@"
  {
    printf '$ kubectl'
    if [[ -n "$CONTEXT" ]]; then
      printf ' --context %q' "$CONTEXT"
    fi
    if [[ -n "$KUBECONFIG_ARG" ]]; then
      printf ' --kubeconfig %q' "$KUBECONFIG_ARG"
    fi
    printf ' %q' "$@"
    printf '\n\n'
    "${KUBECTL[@]}" "$@"
  } > "$path" 2>&1
  local rc=$?
  if [[ $rc -ne 0 ]]; then
    printf '[WARN] command failed with exit %s: %s\n' "$rc" "$rel_path" >&2
  fi
  return 0
}

run_events_tail() {
  local path="$OUT_DIR/pods/events-recent.txt"
  mkdir -p "$(dirname "$path")"
  record_command get events -A --sort-by=.lastTimestamp
  {
    printf '$ kubectl get events -A --sort-by=.lastTimestamp | tail -n %s\n\n' "$EVENT_TAIL"
    "${KUBECTL[@]}" get events -A --sort-by=.lastTimestamp | tail -n "$EVENT_TAIL"
  } > "$path" 2>&1
  return 0
}

echo "Collecting read-only Harvester status into: $OUT_DIR"

run_kubectl auth/can-i-get-nodes.txt auth can-i get nodes
run_kubectl auth/can-i-list-pods-all-namespaces.txt auth can-i list pods -A
run_kubectl auth/can-i-get-storageclasses.txt auth can-i get storageclasses
run_kubectl auth/can-i-get-pvc-all-namespaces.txt auth can-i get persistentvolumeclaims -A
run_kubectl auth/can-i-get-vms-all-namespaces.txt auth can-i get virtualmachines.kubevirt.io -A
run_kubectl auth/can-i-get-longhorn-volumes.txt auth can-i get volumes.longhorn.io -n longhorn-system

run_kubectl cluster/nodes-wide.txt get nodes -o wide
run_kubectl cluster/nodes-describe.txt describe nodes
run_kubectl cluster/nodes-json.txt get nodes -o json
run_kubectl cluster/componentstatuses.txt get componentstatuses
run_kubectl cluster/readyz-verbose.txt get --raw=/readyz?verbose
run_kubectl cluster/livez-verbose.txt get --raw=/livez?verbose
run_kubectl cluster/top-nodes.txt top nodes

run_kubectl pods/namespaces.txt get ns
run_kubectl pods/pods-all-wide.txt get pods -A -o wide
run_kubectl pods/pods-not-running-or-succeeded.txt get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded -o wide
run_kubectl pods/top-pods-all.txt top pods -A
run_events_tail

run_kubectl control-plane/kube-system-pods-wide.txt get pods -n kube-system -o wide
run_kubectl control-plane/default-kubernetes-endpoints.txt get endpoints -n default kubernetes
run_kubectl control-plane/kube-node-lease-leases.txt get leases -n kube-node-lease
run_kubectl control-plane/kube-system-leases.txt get leases -n kube-system

run_kubectl harvester/pods-wide.txt get pods -n harvester-system -o wide
run_kubectl harvester/deployments.txt get deploy -n harvester-system
run_kubectl harvester/daemonsets.txt get daemonset -n harvester-system
run_kubectl harvester/jobs.txt get jobs -n harvester-system
run_kubectl harvester/services.txt get svc -n harvester-system
run_kubectl harvester/ingress-all.txt get ingress -A

run_kubectl vip/ingress-expose-service-yaml.txt -n kube-system get svc ingress-expose -o yaml
run_kubectl vip/kube-vip-pods-selector-wide.txt -n harvester-system get pods -l app.kubernetes.io/name=kube-vip -o wide

run_kubectl vm/virtualmachines.txt get virtualmachines.kubevirt.io -A
run_kubectl vm/virtualmachine-pvc-network-map.tsv get virtualmachines.kubevirt.io -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.status.printableStatus}{"\t"}{.spec.running}{"\t"}{range .spec.template.spec.volumes[*]}{.name}{":pvc="}{.persistentVolumeClaim.claimName}{":dv="}{.dataVolume.name}{";"}{end}{"\t"}{range .spec.template.spec.networks[*]}{.name}{":multus="}{.multus.networkName}{":pod="}{.pod}{";"}{end}{"\n"}{end}'
run_kubectl vm/virtualmachineinstances-wide.txt get virtualmachineinstances.kubevirt.io -A -o wide
run_kubectl vm/virtualmachineinstance-placement.tsv get virtualmachineinstances.kubevirt.io -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.status.phase}{"\t"}{.status.nodeName}{"\t"}{.status.migrationState.phase}{"\n"}{end}'

run_kubectl cdi/datavolumes.txt get datavolumes.cdi.kubevirt.io -A
run_kubectl cdi/datavolume-status.tsv get datavolumes.cdi.kubevirt.io -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.status.phase}{"\t"}{.status.progress}{"\t"}{.spec.pvc.storageClassName}{"\n"}{end}'
run_kubectl cdi/storageprofiles.txt get storageprofile
run_kubectl cdi/storageprofiles-yaml.txt get storageprofile -o yaml

run_kubectl storage/storageclasses.txt get storageclass
run_kubectl storage/storageclasses-yaml.txt get storageclass -o yaml
run_kubectl storage/pvcs-all.txt get pvc -A
run_kubectl storage/pvs.txt get pv
run_kubectl storage/volumesnapshots-all.txt get volumesnapshot -A
run_kubectl storage/volumesnapshotclasses.txt get volumesnapshotclass
run_kubectl storage/volumesnapshotcontents.txt get volumesnapshotcontent

run_kubectl longhorn/pods-wide.txt -n longhorn-system get pods -o wide
run_kubectl longhorn/nodes.txt -n longhorn-system get nodes.longhorn.io
run_kubectl longhorn/nodes-yaml.txt -n longhorn-system get nodes.longhorn.io -o yaml
run_kubectl longhorn/volumes.txt -n longhorn-system get volumes.longhorn.io
run_kubectl longhorn/volumes-yaml.txt -n longhorn-system get volumes.longhorn.io -o yaml
run_kubectl longhorn/replicas.txt -n longhorn-system get replicas.longhorn.io
run_kubectl longhorn/engines.txt -n longhorn-system get engines.longhorn.io
run_kubectl longhorn/settings.txt -n longhorn-system get settings.longhorn.io
run_kubectl longhorn/recurringjobs.txt -n longhorn-system get recurringjobs.longhorn.io
run_kubectl longhorn/backingimages.txt -n longhorn-system get backingimages.longhorn.io

run_kubectl network/network-attachment-definitions.txt get network-attachment-definitions -A
run_kubectl network/ippools.txt get ippools -A
run_kubectl network/kube-system-pods-wide.txt get pods -n kube-system -o wide
run_kubectl network/harvester-system-pods-wide.txt get pods -n harvester-system -o wide

if [[ "$COLLECT_LOGS" -eq 1 ]]; then
  TARGETS="$OUT_DIR/logs/target-pods.tsv"
  "${KUBECTL[@]}" get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.status.phase}{"\t"}{range .status.containerStatuses[*]}{.restartCount}{","}{.state.waiting.reason}{","}{.lastState.terminated.reason}{";"}{end}{"\n"}{end}' \
    | awk -v threshold="$RESTART_THRESHOLD" -F '\t' '
      $3 == "Pending" || $3 == "Failed" || $4 ~ /(CrashLoopBackOff|ImagePullBackOff|ErrImagePull|Error|CreateContainerConfigError|RunContainerError)/ {
        print $1 "\t" $2
        next
      }
      {
        split($4, containers, ";")
        for (idx in containers) {
          split(containers[idx], fields, ",")
          if ((fields[1] + 0) >= threshold) {
            print $1 "\t" $2
            next
          }
        }
      }
    ' | sort -u > "$TARGETS" 2>/dev/null || true

  while IFS=$'\t' read -r namespace pod; do
    [[ -z "$namespace" || -z "$pod" ]] && continue
    safe_name="${namespace}__${pod}"
    run_kubectl "logs/${safe_name}-describe.txt" describe pod -n "$namespace" "$pod"
    run_kubectl "logs/${safe_name}-logs-tail100.txt" logs -n "$namespace" "$pod" --all-containers --tail=100 --prefix
    run_kubectl "logs/${safe_name}-logs-previous-tail100.txt" logs -n "$namespace" "$pod" --all-containers --previous --tail=100 --prefix
  done < "$TARGETS"
fi

cat > "$OUT_DIR/README.txt" <<EOF
Harvester status snapshot collected at $(date -u +%Y-%m-%dT%H:%M:%SZ)

This directory contains read-only kubectl output for cluster status analysis.
Review commands-executed.txt for the exact command list.

No Secret objects were intentionally fetched by this collector.
EOF

echo "Done. Review: $OUT_DIR"
