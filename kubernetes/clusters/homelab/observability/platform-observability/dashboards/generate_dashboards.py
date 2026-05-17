#!/usr/bin/env python3
"""Generate compact Grafana dashboards for the homelab guest cluster."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DS = {"type": "prometheus", "uid": "${datasource}"}
GUEST_DS = {"type": "prometheus", "uid": "${guest_datasource}"}
HARVESTER_DS = {"type": "prometheus", "uid": "${harvester_datasource}"}


def target(
    expr: str,
    ref_id: str = "A",
    legend: str = "",
    instant: bool = False,
    datasource: dict[str, str] = DS,
) -> dict[str, Any]:
    data: dict[str, Any] = {
        "datasource": datasource,
        "editorMode": "code",
        "expr": expr,
        "legendFormat": legend,
        "range": not instant,
        "refId": ref_id,
    }
    if instant:
        data["instant"] = True
    return data


def thresholds(mode: str = "absolute", steps: list[tuple[str, float | None]] | None = None) -> dict[str, Any]:
    if steps is None:
        steps = [("green", None)]
    return {"mode": mode, "steps": [{"color": color, "value": value} for color, value in steps]}


def panel(
    panel_id: int,
    title: str,
    ptype: str,
    x: int,
    y: int,
    w: int,
    h: int,
    exprs: list[dict[str, Any]],
    *,
    unit: str = "short",
    description: str = "",
    decimals: int | None = None,
    stacked: bool = False,
    legend: bool = True,
    reduce_calc: str = "lastNotNull",
    datasource: dict[str, str] = DS,
) -> dict[str, Any]:
    options: dict[str, Any]
    if ptype == "stat":
        options = {
            "colorMode": "value",
            "graphMode": "area",
            "justifyMode": "auto",
            "orientation": "auto",
            "reduceOptions": {"calcs": [reduce_calc], "fields": "", "values": False},
            "showPercentChange": False,
            "textMode": "auto",
            "wideLayout": True,
        }
    elif ptype == "table":
        options = {
            "cellHeight": "sm",
            "footer": {"countRows": False, "fields": "", "reducer": ["sum"], "show": False},
            "showHeader": True,
        }
    elif ptype == "bargauge":
        options = {
            "displayMode": "gradient",
            "maxVizHeight": 300,
            "minVizHeight": 16,
            "minVizWidth": 8,
            "namePlacement": "auto",
            "orientation": "horizontal",
            "reduceOptions": {"calcs": [reduce_calc], "fields": "", "values": False},
            "showUnfilled": True,
            "sizing": "auto",
            "valueMode": "color",
        }
    else:
        options = {
            "legend": {"calcs": [], "displayMode": "list", "placement": "bottom", "showLegend": legend},
            "tooltip": {"hideZeros": False, "mode": "multi", "sort": "none"},
        }

    custom: dict[str, Any] = {}
    if ptype == "timeseries":
        custom = {
            "drawStyle": "line",
            "fillOpacity": 12 if stacked else 0,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "showPoints": "never",
            "spanNulls": False,
            "stacking": {"group": "A", "mode": "normal" if stacked else "none"},
        }

    defaults: dict[str, Any] = {
        "color": {"mode": "palette-classic"},
        "mappings": [],
        "thresholds": thresholds(),
        "unit": unit,
    }
    if decimals is not None:
        defaults["decimals"] = decimals
    if custom:
        defaults["custom"] = custom

    return {
        "datasource": datasource,
        "description": description,
        "fieldConfig": {"defaults": defaults, "overrides": []},
        "gridPos": {"h": h, "w": w, "x": x, "y": y},
        "id": panel_id,
        "options": options,
        "targets": exprs,
        "title": title,
        "type": ptype,
    }


def datasource_var(name: str = "datasource", text: str = "VictoriaMetrics", value: str = "VictoriaMetrics") -> dict[str, Any]:
    return {
        "current": {"selected": False, "text": text, "value": value},
        "hide": 0,
        "name": name,
        "options": [],
        "query": "prometheus",
        "refresh": 1,
        "regex": "",
        "skipUrlSync": False,
        "type": "datasource",
    }


def query_var(
    name: str,
    label_query: str,
    *,
    include_all: bool = True,
    multi: bool = True,
    datasource: dict[str, str] = DS,
) -> dict[str, Any]:
    return {
        "current": {"selected": False, "text": "All" if include_all else "", "value": "$__all" if include_all else ""},
        "datasource": datasource,
        "definition": label_query,
        "hide": 0,
        "includeAll": include_all,
        "multi": multi,
        "name": name,
        "options": [],
        "query": {"qryType": 1, "query": label_query, "refId": f"Variable-{name}"},
        "refresh": 1,
        "regex": "",
        "skipUrlSync": False,
        "sort": 1,
        "type": "query",
    }


def dashboard(
    uid: str,
    title: str,
    tags: list[str],
    panels: list[dict[str, Any]],
    variables: list[dict[str, Any]],
    datasource_variables: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    datasource_variables = datasource_variables if datasource_variables is not None else [datasource_var()]
    return {
        "annotations": {"list": [{"builtIn": 1, "datasource": {"type": "grafana", "uid": "-- Grafana --"}, "enable": True, "hide": True, "iconColor": "rgba(0, 211, 255, 1)", "name": "Annotations & Alerts", "type": "dashboard"}]},
        "editable": True,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 0,
        "id": None,
        "links": [],
        "panels": panels,
        "refresh": "30s",
        "schemaVersion": 42,
        "tags": tags,
        "templating": {"list": [*datasource_variables, *variables]},
        "time": {"from": "now-1h", "to": "now"},
        "timepicker": {},
        "timezone": "browser",
        "title": title,
        "uid": uid,
        "version": 1,
        "weekStart": "",
    }


def write(name: str, data: dict[str, Any]) -> None:
    (ROOT / name).write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")


def build() -> None:
    ns_var = query_var("namespace", "label_values(kube_namespace_created, namespace)")
    node_var = query_var("node", "label_values(kube_node_info, node)")
    pod_var = query_var("pod", 'label_values(kube_pod_info{namespace=~"$namespace"}, pod)')
    workload_var = query_var("workload", 'label_values(kube_deployment_labels{namespace=~"$namespace"}, deployment)')
    sc_var = query_var("storageclass", "label_values(kube_storageclass_info, storageclass)")
    pvc_var = query_var("persistentvolumeclaim", 'label_values(kube_persistentvolumeclaim_info{namespace=~"$namespace"}, persistentvolumeclaim)')
    guest_ns_var = query_var("namespace", "label_values(kube_namespace_created, namespace)", datasource=GUEST_DS)
    guest_pvc_var = query_var(
        "persistentvolumeclaim",
        'label_values(kube_persistentvolumeclaim_info{namespace=~"$namespace"}, persistentvolumeclaim)',
        datasource=GUEST_DS,
    )
    longhorn_volume_var = query_var(
        "longhorn_volume",
        'label_values(longhorn_volume_state{pvc_namespace=~"$namespace",pvc=~"$persistentvolumeclaim"}, volume)',
        datasource=HARVESTER_DS,
    )
    longhorn_node_var = query_var("longhorn_node", "label_values(longhorn_node_status, node)", datasource=HARVESTER_DS)
    longhorn_disk_var = query_var(
        "longhorn_disk",
        'label_values(longhorn_disk_capacity_bytes{node=~"$longhorn_node"}, disk)',
        datasource=HARVESTER_DS,
    )

    write(
        "guest-cluster-overview.json",
        dashboard(
            "homelab-guest-cluster-overview",
            "Homelab / Guest Cluster Overview",
            ["homelab", "overview", "guest-kubernetes"],
            [
                panel(1, "Ready Nodes", "stat", 0, 0, 4, 4, [target('count(kube_node_status_condition{condition="Ready",status="true"} == 1)', instant=True)], unit="short"),
                panel(2, "Non-Running Pods", "stat", 4, 0, 4, 4, [target('count(kube_pod_status_phase{phase=~"Pending|Failed|Unknown"} == 1)', instant=True)], unit="short"),
                panel(3, "PVCs Not Bound", "stat", 8, 0, 4, 4, [target('count(kube_persistentvolumeclaim_status_phase{phase!="Bound"} == 1)', instant=True)], unit="short"),
                panel(4, "Scrape Targets Down", "stat", 12, 0, 4, 4, [target("count(up == 0)", instant=True)], unit="short"),
                panel(5, "Argo Apps Not Healthy", "stat", 16, 0, 4, 4, [target('count(argocd_app_info{health_status!="Healthy"})', instant=True)], unit="short"),
                panel(6, "ExternalSecret Problems", "stat", 20, 0, 4, 4, [target('count(externalsecret_status_condition{status!="True"} == 1)', instant=True)], unit="short"),
                panel(7, "Cluster CPU By Node", "timeseries", 0, 4, 12, 8, [target('sum by (instance) (rate(node_cpu_seconds_total{mode!="idle"}[5m]))', legend="{{instance}}")], unit="cores"),
                panel(8, "Cluster Memory By Node", "timeseries", 12, 4, 12, 8, [target('sum by (instance) (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)', legend="{{instance}}")], unit="bytes"),
                panel(9, "Pods By Namespace", "bargauge", 0, 12, 8, 8, [target('count by (namespace) (kube_pod_info{namespace=~"$namespace"})', instant=True)], unit="short"),
                panel(10, "CPU By Namespace", "timeseries", 8, 12, 8, 8, [target('sum by (namespace) (rate(container_cpu_usage_seconds_total{namespace=~"$namespace",container!="",image!=""}[5m]))', legend="{{namespace}}")], unit="cores", stacked=True),
                panel(11, "Memory By Namespace", "timeseries", 16, 12, 8, 8, [target('sum by (namespace) (container_memory_working_set_bytes{namespace=~"$namespace",container!="",image!=""})', legend="{{namespace}}")], unit="bytes", stacked=True),
                panel(12, "Top Restarting Containers", "table", 0, 20, 12, 8, [target('topk(15, sum by (namespace,pod,container) (increase(kube_pod_container_status_restarts_total[1h])))', instant=True)], unit="short"),
                panel(13, "Down Scrape Targets", "table", 12, 20, 12, 8, [target("up == 0", instant=True)], unit="short"),
            ],
            [ns_var],
        ),
    )

    write(
        "node-overview.json",
        dashboard(
            "homelab-node-overview",
            "Homelab / Node Overview",
            ["homelab", "nodes", "guest-kubernetes"],
            [
                panel(1, "Node Ready", "stat", 0, 0, 6, 4, [target('kube_node_status_condition{node=~"$node",condition="Ready",status="true"}', legend="{{node}}", instant=True)], unit="short"),
                panel(2, "Node CPU Cores Used", "timeseries", 0, 4, 12, 8, [target('sum by (instance) (rate(node_cpu_seconds_total{instance=~"$node",mode!="idle"}[5m]))', legend="{{instance}}")], unit="cores"),
                panel(3, "Node Memory Used", "timeseries", 12, 4, 12, 8, [target('sum by (instance) (node_memory_MemTotal_bytes{instance=~"$node"} - node_memory_MemAvailable_bytes{instance=~"$node"})', legend="{{instance}}")], unit="bytes"),
                panel(4, "Filesystem Available", "timeseries", 0, 12, 12, 8, [target('node_filesystem_avail_bytes{instance=~"$node",fstype!~"tmpfs|overlay",mountpoint!~"/run.*|/var/lib/kubelet/pods.*"}', legend="{{instance}} {{mountpoint}}")], unit="bytes"),
                panel(5, "Network Receive", "timeseries", 12, 12, 6, 8, [target('sum by (instance,device) (rate(node_network_receive_bytes_total{instance=~"$node",device!~"lo|veth.*|flannel.*|cni.*"}[5m]))', legend="{{instance}} {{device}}")], unit="Bps"),
                panel(6, "Network Transmit", "timeseries", 18, 12, 6, 8, [target('sum by (instance,device) (rate(node_network_transmit_bytes_total{instance=~"$node",device!~"lo|veth.*|flannel.*|cni.*"}[5m]))', legend="{{instance}} {{device}}")], unit="Bps"),
                panel(7, "Node Pressure Conditions", "table", 0, 20, 12, 8, [target('kube_node_status_condition{node=~"$node",condition=~"DiskPressure|MemoryPressure|PIDPressure|NetworkUnavailable",status="true"}', instant=True)], unit="short"),
                panel(8, "Pods Per Node", "bargauge", 12, 20, 12, 8, [target('count by (node) (kube_pod_info{node=~"$node"})', instant=True)], unit="short"),
            ],
            [node_var],
        ),
    )

    write(
        "namespace-workload-overview.json",
        dashboard(
            "homelab-namespace-workload-overview",
            "Homelab / Namespace & Workload Overview",
            ["homelab", "workloads", "namespaces"],
            [
                panel(1, "Pods By Phase", "bargauge", 0, 0, 8, 6, [target('sum by (namespace,phase) (kube_pod_status_phase{namespace=~"$namespace"} == 1)', instant=True)], unit="short"),
                panel(2, "Deployment Available Replicas", "table", 8, 0, 8, 6, [target('kube_deployment_status_replicas_available{namespace=~"$namespace",deployment=~"$workload"}', instant=True)], unit="short"),
                panel(3, "Unavailable Deployment Replicas", "stat", 16, 0, 8, 6, [target('sum(kube_deployment_status_replicas_unavailable{namespace=~"$namespace",deployment=~"$workload"})', instant=True)], unit="short"),
                panel(4, "CPU By Namespace", "timeseries", 0, 6, 12, 8, [target('sum by (namespace) (rate(container_cpu_usage_seconds_total{namespace=~"$namespace",container!="",image!=""}[5m]))', legend="{{namespace}}")], unit="cores", stacked=True),
                panel(5, "Memory By Namespace", "timeseries", 12, 6, 12, 8, [target('sum by (namespace) (container_memory_working_set_bytes{namespace=~"$namespace",container!="",image!=""})', legend="{{namespace}}")], unit="bytes", stacked=True),
                panel(6, "CPU By Pod", "timeseries", 0, 14, 12, 8, [target('sum by (namespace,pod) (rate(container_cpu_usage_seconds_total{namespace=~"$namespace",pod=~"$pod",container!="",image!=""}[5m]))', legend="{{namespace}}/{{pod}}")], unit="cores"),
                panel(7, "Memory By Pod", "timeseries", 12, 14, 12, 8, [target('sum by (namespace,pod) (container_memory_working_set_bytes{namespace=~"$namespace",pod=~"$pod",container!="",image!=""})', legend="{{namespace}}/{{pod}}")], unit="bytes"),
                panel(8, "Restarting Containers", "table", 0, 22, 12, 8, [target('topk(20, sum by (namespace,pod,container) (increase(kube_pod_container_status_restarts_total{namespace=~"$namespace",pod=~"$pod"}[1h])))', instant=True)], unit="short"),
                panel(9, "Pending Or Failed Pods", "table", 12, 22, 12, 8, [target('kube_pod_status_phase{namespace=~"$namespace",pod=~"$pod",phase=~"Pending|Failed|Unknown"} == 1', instant=True)], unit="short"),
            ],
            [ns_var, workload_var, pod_var],
        ),
    )

    write(
        "storage-csi-object-state.json",
        dashboard(
            "homelab-storage-csi-object-state",
            "Homelab / Storage & CSI Object State",
            ["homelab", "storage", "csi"],
            [
                panel(1, "PVCs Not Bound", "stat", 0, 0, 6, 4, [target('count(kube_persistentvolumeclaim_status_phase{namespace=~"$namespace",persistentvolumeclaim=~"$persistentvolumeclaim",phase!="Bound"} == 1)', instant=True)], unit="short"),
                panel(2, "VolumeAttachments Not Attached", "stat", 6, 0, 6, 4, [target("count(kube_volumeattachment_status_attached == 0)", instant=True)], unit="short"),
                panel(3, "CSI Pod Restarts Last Hour", "stat", 12, 0, 6, 4, [target('sum(increase(kube_pod_container_status_restarts_total{namespace="kube-system",pod=~"harvester-csi-driver.*"}[1h]))', instant=True)], unit="short"),
                panel(4, "PVC Phase", "table", 0, 4, 12, 8, [target('kube_persistentvolumeclaim_status_phase{namespace=~"$namespace",persistentvolumeclaim=~"$persistentvolumeclaim"} == 1', instant=True)], unit="short"),
                panel(5, "PV Phase", "table", 12, 4, 12, 8, [target("kube_persistentvolume_status_phase == 1", instant=True)], unit="short"),
                panel(6, "PVC Capacity", "timeseries", 0, 12, 8, 8, [target('kubelet_volume_stats_capacity_bytes{namespace=~"$namespace",persistentvolumeclaim=~"$persistentvolumeclaim"}', legend="{{namespace}}/{{persistentvolumeclaim}}")], unit="bytes"),
                panel(7, "PVC Used", "timeseries", 8, 12, 8, 8, [target('kubelet_volume_stats_used_bytes{namespace=~"$namespace",persistentvolumeclaim=~"$persistentvolumeclaim"}', legend="{{namespace}}/{{persistentvolumeclaim}}")], unit="bytes"),
                panel(8, "PVC Available", "timeseries", 16, 12, 8, 8, [target('kubelet_volume_stats_available_bytes{namespace=~"$namespace",persistentvolumeclaim=~"$persistentvolumeclaim"}', legend="{{namespace}}/{{persistentvolumeclaim}}")], unit="bytes"),
                panel(9, "StorageClasses", "table", 0, 20, 8, 8, [target('kube_storageclass_info{storageclass=~"$storageclass"}', instant=True)], unit="short"),
                panel(10, "VolumeAttachment State", "table", 8, 20, 8, 8, [target("kube_volumeattachment_status_attached", instant=True)], unit="short"),
                panel(11, "Harvester CSI Pods", "table", 16, 20, 8, 8, [target('kube_pod_status_phase{namespace="kube-system",pod=~"harvester-csi-driver.*"} == 1', instant=True)], unit="short"),
            ],
            [ns_var, pvc_var, sc_var],
        ),
    )

    write(
        "storage-csi-performance.json",
        dashboard(
            "homelab-storage-csi-performance",
            "Homelab / Storage & CSI Performance",
            ["homelab", "storage", "csi", "longhorn", "performance"],
            [
                panel(1, "PVCs Not Bound", "stat", 0, 0, 4, 4, [target('count(kube_persistentvolumeclaim_status_phase{namespace=~"$namespace",persistentvolumeclaim=~"$persistentvolumeclaim",phase!="Bound"} == 1)', instant=True, datasource=GUEST_DS)], unit="short", datasource=GUEST_DS),
                panel(2, "VolumeAttachments Not Attached", "stat", 4, 0, 4, 4, [target("count(kube_volumeattachment_status_attached == 0)", instant=True, datasource=GUEST_DS)], unit="short", datasource=GUEST_DS),
                panel(3, "CSI Restarts Last Hour", "stat", 8, 0, 4, 4, [target('sum(increase(kube_pod_container_status_restarts_total{namespace="kube-system",pod=~"harvester-csi-driver.*"}[1h]))', instant=True, datasource=GUEST_DS)], unit="short", datasource=GUEST_DS),
                panel(4, "PVC Used Percent", "stat", 12, 0, 4, 4, [target('100 * sum(kubelet_volume_stats_used_bytes{namespace=~"$namespace",persistentvolumeclaim=~"$persistentvolumeclaim"}) / sum(kubelet_volume_stats_capacity_bytes{namespace=~"$namespace",persistentvolumeclaim=~"$persistentvolumeclaim"})', instant=True, datasource=GUEST_DS)], unit="percent", decimals=1, datasource=GUEST_DS),
                panel(5, "Longhorn Volumes Degraded", "stat", 16, 0, 4, 4, [target('count(longhorn_volume_robustness{pvc_namespace=~"$namespace",pvc=~"$persistentvolumeclaim",volume=~"$longhorn_volume",state!~"healthy|unknown"} == 1)', instant=True, datasource=HARVESTER_DS)], unit="short", datasource=HARVESTER_DS),
                panel(6, "Longhorn Nodes Down", "stat", 20, 0, 4, 4, [target('count(longhorn_node_status{node=~"$longhorn_node",condition="ready"} == 0)', instant=True, datasource=HARVESTER_DS)], unit="short", datasource=HARVESTER_DS),
                panel(7, "Longhorn Volume Throughput", "timeseries", 0, 4, 12, 8, [
                    target('sum by (volume,pvc_namespace,pvc,node) (longhorn_volume_read_throughput{pvc_namespace=~"$namespace",pvc=~"$persistentvolumeclaim",volume=~"$longhorn_volume"})', "A", "read {{pvc_namespace}}/{{pvc}} {{volume}} {{node}}", datasource=HARVESTER_DS),
                    target('sum by (volume,pvc_namespace,pvc,node) (longhorn_volume_write_throughput{pvc_namespace=~"$namespace",pvc=~"$persistentvolumeclaim",volume=~"$longhorn_volume"})', "B", "write {{pvc_namespace}}/{{pvc}} {{volume}} {{node}}", datasource=HARVESTER_DS),
                ], unit="Bps", datasource=HARVESTER_DS),
                panel(8, "Longhorn Volume IOPS", "timeseries", 12, 4, 12, 8, [
                    target('sum by (volume,pvc_namespace,pvc,node) (longhorn_volume_read_iops{pvc_namespace=~"$namespace",pvc=~"$persistentvolumeclaim",volume=~"$longhorn_volume"})', "A", "read {{pvc_namespace}}/{{pvc}} {{volume}} {{node}}", datasource=HARVESTER_DS),
                    target('sum by (volume,pvc_namespace,pvc,node) (longhorn_volume_write_iops{pvc_namespace=~"$namespace",pvc=~"$persistentvolumeclaim",volume=~"$longhorn_volume"})', "B", "write {{pvc_namespace}}/{{pvc}} {{volume}} {{node}}", datasource=HARVESTER_DS),
                ], unit="iops", datasource=HARVESTER_DS),
                panel(9, "Longhorn Volume Latency", "timeseries", 0, 12, 12, 8, [
                    target('avg by (volume,pvc_namespace,pvc,node) (longhorn_volume_read_latency{pvc_namespace=~"$namespace",pvc=~"$persistentvolumeclaim",volume=~"$longhorn_volume"}) / 1000000', "A", "read {{pvc_namespace}}/{{pvc}} {{volume}} {{node}}", datasource=HARVESTER_DS),
                    target('avg by (volume,pvc_namespace,pvc,node) (longhorn_volume_write_latency{pvc_namespace=~"$namespace",pvc=~"$persistentvolumeclaim",volume=~"$longhorn_volume"}) / 1000000', "B", "write {{pvc_namespace}}/{{pvc}} {{volume}} {{node}}", datasource=HARVESTER_DS),
                ], unit="ms", decimals=2, datasource=HARVESTER_DS),
                panel(10, "Longhorn Volume Size", "timeseries", 12, 12, 12, 8, [
                    target('longhorn_volume_actual_size_bytes{pvc_namespace=~"$namespace",pvc=~"$persistentvolumeclaim",volume=~"$longhorn_volume"}', "A", "actual {{pvc_namespace}}/{{pvc}} {{volume}}", datasource=HARVESTER_DS),
                    target('longhorn_volume_capacity_bytes{pvc_namespace=~"$namespace",pvc=~"$persistentvolumeclaim",volume=~"$longhorn_volume"}', "B", "capacity {{pvc_namespace}}/{{pvc}} {{volume}}", datasource=HARVESTER_DS),
                ], unit="bytes", datasource=HARVESTER_DS),
                panel(11, "PVC Capacity And Usage", "timeseries", 0, 20, 12, 8, [
                    target('kubelet_volume_stats_used_bytes{namespace=~"$namespace",persistentvolumeclaim=~"$persistentvolumeclaim"}', "A", "used {{namespace}}/{{persistentvolumeclaim}}", datasource=GUEST_DS),
                    target('kubelet_volume_stats_available_bytes{namespace=~"$namespace",persistentvolumeclaim=~"$persistentvolumeclaim"}', "B", "available {{namespace}}/{{persistentvolumeclaim}}", datasource=GUEST_DS),
                    target('kubelet_volume_stats_capacity_bytes{namespace=~"$namespace",persistentvolumeclaim=~"$persistentvolumeclaim"}', "C", "capacity {{namespace}}/{{persistentvolumeclaim}}", datasource=GUEST_DS),
                ], unit="bytes", datasource=GUEST_DS),
                panel(12, "Pod CPU And Memory Near PVC Namespace", "timeseries", 12, 20, 12, 8, [
                    target('sum by (namespace,pod) (rate(container_cpu_usage_seconds_total{namespace=~"$namespace",container!="",image!=""}[5m]))', "A", "cpu {{namespace}}/{{pod}}", datasource=GUEST_DS),
                    target('sum by (namespace,pod) (container_memory_working_set_bytes{namespace=~"$namespace",container!="",image!=""}) / 1073741824', "B", "memory Gi {{namespace}}/{{pod}}", datasource=GUEST_DS),
                ], unit="short", datasource=GUEST_DS),
                panel(13, "PVC To PV Mapping", "table", 0, 28, 8, 8, [target('kube_persistentvolumeclaim_info{namespace=~"$namespace",persistentvolumeclaim=~"$persistentvolumeclaim"}', instant=True, datasource=GUEST_DS)], unit="short", datasource=GUEST_DS),
                panel(14, "VolumeAttachment Mapping", "table", 8, 28, 8, 8, [target("kube_volumeattachment_spec_source_persistentvolume", instant=True, datasource=GUEST_DS)], unit="short", datasource=GUEST_DS),
                panel(15, "Longhorn Volume State", "table", 16, 28, 8, 8, [target('longhorn_volume_state{pvc_namespace=~"$namespace",pvc=~"$persistentvolumeclaim",volume=~"$longhorn_volume"} == 1', instant=True, datasource=HARVESTER_DS)], unit="short", datasource=HARVESTER_DS),
                panel(16, "Longhorn Volume Robustness", "table", 0, 36, 8, 8, [target('longhorn_volume_robustness{pvc_namespace=~"$namespace",pvc=~"$persistentvolumeclaim",volume=~"$longhorn_volume"} == 1', instant=True, datasource=HARVESTER_DS)], unit="short", datasource=HARVESTER_DS),
                panel(17, "Longhorn Disk Usage Percent", "bargauge", 8, 36, 8, 8, [target('100 * sum by (node,disk) (longhorn_disk_usage_bytes{node=~"$longhorn_node",disk=~"$longhorn_disk"}) / sum by (node,disk) (longhorn_disk_capacity_bytes{node=~"$longhorn_node",disk=~"$longhorn_disk"})', instant=True, datasource=HARVESTER_DS)], unit="percent", decimals=1, datasource=HARVESTER_DS),
                panel(18, "Longhorn Disk Status And Health", "table", 16, 36, 8, 8, [target('longhorn_disk_status{node=~"$longhorn_node",disk=~"$longhorn_disk"}', "A", instant=True, datasource=HARVESTER_DS), target('longhorn_disk_health{node=~"$longhorn_node",disk=~"$longhorn_disk"}', "B", instant=True, datasource=HARVESTER_DS)], unit="short", datasource=HARVESTER_DS),
            ],
            [guest_ns_var, guest_pvc_var, longhorn_volume_var, longhorn_node_var, longhorn_disk_var],
            datasource_variables=[
                datasource_var("guest_datasource", "VictoriaMetrics", "VictoriaMetrics"),
                datasource_var("harvester_datasource", "Harvester Prometheus", "Harvester Prometheus"),
            ],
        ),
    )

    write(
        "control-plane-dns.json",
        dashboard(
            "homelab-control-plane-dns",
            "Homelab / Control Plane & DNS",
            ["homelab", "control-plane", "dns"],
            [
                panel(1, "API Servers Up", "stat", 0, 0, 6, 4, [target('count(up{job="apiserver"} == 1)', instant=True)], unit="short"),
                panel(2, "CoreDNS Pods Up", "stat", 6, 0, 6, 4, [target('count(up{job="kube-dns"} == 1)', instant=True)], unit="short"),
                panel(3, "Kubelet Scrapes Down", "stat", 12, 0, 6, 4, [target('count(up{job="kubelet"} == 0)', instant=True)], unit="short"),
                panel(4, "API Request Rate", "timeseries", 0, 4, 12, 8, [target('sum by (instance,verb) (rate(apiserver_request_total[5m]))', legend="{{instance}} {{verb}}")], unit="reqps"),
                panel(5, "API p95 Latency", "timeseries", 12, 4, 12, 8, [target('histogram_quantile(0.95, sum by (le,instance) (rate(apiserver_request_duration_seconds_bucket[5m])))', legend="{{instance}}")], unit="s"),
                panel(6, "API Inflight Requests", "timeseries", 0, 12, 8, 8, [target('sum by (instance,request_kind) (apiserver_current_inflight_requests)', legend="{{instance}} {{request_kind}}")], unit="short"),
                panel(7, "CoreDNS Request Rate", "timeseries", 8, 12, 8, 8, [target('sum by (pod,type) (rate(coredns_dns_requests_total[5m]))', legend="{{pod}} {{type}}")], unit="reqps"),
                panel(8, "CoreDNS p95 Latency", "timeseries", 16, 12, 8, 8, [target('histogram_quantile(0.95, sum by (le,pod) (rate(coredns_dns_request_duration_seconds_bucket[5m])))', legend="{{pod}}")], unit="s"),
                panel(9, "CoreDNS Response Codes", "timeseries", 0, 20, 12, 8, [target('sum by (rcode) (rate(coredns_dns_responses_total[5m]))', legend="{{rcode}}")], unit="reqps", stacked=True),
                panel(10, "Kubelet Health By Node", "table", 12, 20, 12, 8, [target('up{job="kubelet"}', instant=True)], unit="short"),
            ],
            [],
        ),
    )

    write(
        "gitops-secrets.json",
        dashboard(
            "homelab-gitops-secrets",
            "Homelab / GitOps & Secrets",
            ["homelab", "argocd", "external-secrets"],
            [
                panel(1, "Argo Apps Not Healthy", "stat", 0, 0, 6, 4, [target('count(argocd_app_info{health_status!="Healthy"})', instant=True)], unit="short"),
                panel(2, "Argo Apps Out Of Sync", "stat", 6, 0, 6, 4, [target('count(argocd_app_info{sync_status!="Synced"})', instant=True)], unit="short"),
                panel(3, "ExternalSecrets Not Ready", "stat", 12, 0, 6, 4, [target('count(externalsecret_status_condition{condition="Ready",status!="True"} == 1)', instant=True)], unit="short"),
                panel(4, "SecretStores Not Ready", "stat", 18, 0, 6, 4, [target('count(clustersecretstore_status_condition{condition="Ready",status!="True"} == 1)', instant=True)], unit="short"),
                panel(5, "Argo App Inventory", "table", 0, 4, 12, 8, [target("argocd_app_info", instant=True)], unit="short"),
                panel(6, "Argo Sync Activity", "timeseries", 12, 4, 12, 8, [target("sum by (name,phase) (rate(argocd_app_sync_total[5m]))", legend="{{name}} {{phase}}")], unit="ops"),
                panel(7, "Argo Reconcile p95", "timeseries", 0, 12, 12, 8, [target("histogram_quantile(0.95, sum by (le) (rate(argocd_app_reconcile_bucket[5m])))", legend="p95")], unit="s"),
                panel(8, "ExternalSecret Conditions", "table", 12, 12, 12, 8, [target("externalsecret_status_condition", instant=True)], unit="short"),
                panel(9, "ExternalSecret Provider Calls", "timeseries", 0, 20, 12, 8, [target("sum by (provider,call) (rate(externalsecret_provider_api_calls_count[5m]))", legend="{{provider}} {{call}}")], unit="ops"),
                panel(10, "GitOps/Secret Scrape Targets", "table", 12, 20, 12, 8, [target('up{job=~"argocd.*|observability/external-secrets"}', instant=True)], unit="short"),
            ],
            [],
        ),
    )


if __name__ == "__main__":
    build()
