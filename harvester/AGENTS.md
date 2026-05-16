# Harvester Operating Guide

## Scope

This directory owns Harvester-side desired state: VM definitions, images, VM networks, storage classes, and operator notes for VMs that host Talos, data services, or administrative workloads.

## VM desired-state rules

- Keep manifests focused on desired state. Do not commit live runtime fields such as `status`, `managedFields`, `uid`, or `resourceVersion`.
- Record VM name, namespace, CPU, memory, disks, storage class, network attachment, boot order, and intended host placement.
- Treat generated VM exports as input to clean up, not as final source of truth.

## Placement rules

- Do not assume a VM will stay on a Harvester node unless affinity, node selector, or another placement rule exists.
- State the intended host for each durable VM and explain the reason: control-plane HA, worker balance, storage locality, or data locality.
- For node-local disks or large data volumes, placement is part of the design, not an implementation detail.

## Talos ISO and boot rules

- Treat Talos ISO attachment as temporary after installation.
- After Talos install, prefer OS disk first and remove or disable ISO boot paths.
- A VM that boots back into the installer/live environment is a recovery condition; inspect boot order, attached CD-ROMs, VMI placement, and Talos network state before changing unrelated settings.

## Safe VM mutation rules

- Prefer dry-run validation before live VM changes.
- For live VM changes, define an explicit stop condition before mutation.
- Do not start, stop, restart, delete, resize, or migrate VMs without explicit approval for that gate.
- After any approved live change, verify Harvester VM state, VMI placement, guest IP, Talos reachability when relevant, and Kubernetes node health when relevant.

## Required reporting

For every VM change, report:

- VM name and namespace
- Intended and actual node placement
- CPU, memory, OS disk, data disks, and storage class
- Network attachment and planned IP
- Boot order and ISO attachment status
- Whether live state changed
- Validation result and next stop gate
