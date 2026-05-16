# Network Map

This file provides the current logical network map for the home lab.

## Current Physical Topology

```mermaid
flowchart TB
  internet["Internet"]
  att["AT&T Router<br/>Gateway: 192.168.1.254"]
  usw["USW-Aggregation<br/>Management IP: TBD"]

  abundance["the-abundance<br/>Harvester node<br/>192.168.1.241<br/>10G SFP+"]
  elation["the-elation<br/>Harvester node<br/>192.168.1.250<br/>10G SFP+"]
  enigmata["the-enigmata<br/>Harvester node<br/>192.168.1.244<br/>1G RJ45"]

  harvesterVip["Harvester VIP/UI<br/>192.168.1.50"]

  internet --> att
  att -->|"sfp8, RJ45 via module"| usw
  usw -->|"sfp1, 10G DAC"| abundance
  usw -->|"sfp2, 10G DAC"| elation
  usw -->|"sfp3, 1G RJ45 module"| enigmata
  abundance -.-> harvesterVip
  elation -.-> harvesterVip
  enigmata -.-> harvesterVip
```

## Harvester And Talos Logical Topology

```mermaid
flowchart TB
  subgraph physical["Physical Nodes"]
    abundance["the-abundance<br/>192.168.1.241"]
    elation["the-elation<br/>192.168.1.250"]
    enigmata["the-enigmata<br/>192.168.1.244"]
  end

  subgraph harvester["Harvester"]
    vip["Harvester VIP/UI<br/>192.168.1.50"]
    mgmt["Cluster Network: mgmt"]
    vmnet["VM Network: lan-untagged"]
    hpods["Harvester Pod CIDR<br/>10.52.0.0/16"]
    hsvcs["Harvester Service CIDR<br/>10.53.0.0/16"]
  end

  subgraph talos["Talos / Kubernetes VMs"]
    api["homelab-talos-api<br/>planned VIP<br/>192.168.1.184"]
    cp["cp-01<br/>control-plane<br/>192.168.1.181"]
    cp2["cp-02<br/>control-plane planned<br/>192.168.1.182"]
    cp3["cp-03<br/>control-plane planned<br/>192.168.1.183"]
    w1["worker-01<br/>Medium worker<br/>IP proposed: 192.168.1.179"]
    w2["worker-02<br/>Small worker<br/>IP proposed: 192.168.1.180"]
  end

  subgraph data["Dedicated Data VMs"]
    data01["data-01<br/>ClickHouse / graph planned<br/>IP TBD"]
  end

  subgraph k8s["homelab-talos Kubernetes"]
    pods["Pod CIDR<br/>10.42.0.0/16"]
    svcs["Service CIDR<br/>10.43.0.0/16"]
  end

  abundance --> vip
  elation --> vip
  enigmata --> vip
  vip --> mgmt
  mgmt --> vmnet
  abundance --> cp
  elation --> cp2
  enigmata --> cp3
  elation --> w1
  enigmata --> w2
  abundance --> data01
  api --> cp
  api --> cp2
  api --> cp3
  cp --> pods
  cp2 --> pods
  cp3 --> pods
  cp --> svcs
  w1 --> pods
  w2 --> pods
  hpods -. separate .- pods
  hsvcs -. separate .- svcs
```

## Current Assumptions

- The home lab is on a flat `192.168.1.0/24` LAN for now.
- No dedicated firewall/router is planned yet.
- AT&T router remains the default gateway.
- `the-abundance`, `the-elation`, and `the-enigmata` are the three verified physical Harvester nodes.
- `cp-01` is the active Talos control-plane VM on `the-abundance`.
- Old `talos-cp-01` has been retired; `192.168.1.178` should be checked before reuse.
- One worker VM per remaining physical node is planned.
- Older references to `the-remembrance` are stale unless that host is reintroduced later.
