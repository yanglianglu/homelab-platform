# Network Map

This file provides the current logical network map for the home lab.

## Current Physical Topology

```mermaid
flowchart TB
  internet["Internet"]
  att["AT&T Router<br/>Gateway: 192.168.1.254"]
  usw["USW-Aggregation<br/>Management IP: TBD"]

  abundance["the-abundance<br/>Harvester node<br/>192.168.1.241<br/>10G SFP+"]
  elation["the-elation<br/>Harvester node<br/>IP: TBD<br/>10G SFP+"]
  remembrance["the-remembrance<br/>Harvester node<br/>IP: TBD<br/>1G RJ45"]

  harvesterVip["Harvester VIP/UI<br/>192.168.1.50"]

  internet --> att
  att -->|"sfp8, RJ45 via module"| usw
  usw -->|"sfp1, 10G DAC"| abundance
  usw -->|"sfp2, 10G DAC"| elation
  usw -->|"sfp3, 1G RJ45 module"| remembrance
  abundance -.-> harvesterVip
  elation -.-> harvesterVip
  remembrance -.-> harvesterVip
```

## Harvester And Talos Logical Topology

```mermaid
flowchart TB
  subgraph physical["Physical Nodes"]
    abundance["the-abundance<br/>192.168.1.241"]
    elation["the-elation<br/>IP TBD"]
    remembrance["the-remembrance<br/>IP TBD"]
  end

  subgraph harvester["Harvester"]
    vip["Harvester VIP/UI<br/>192.168.1.50"]
    mgmt["Cluster Network: mgmt"]
    vmnet["VM Network: lan-untagged"]
    hpods["Harvester Pod CIDR<br/>10.52.0.0/16"]
    hsvcs["Harvester Service CIDR<br/>10.53.0.0/16"]
  end

  subgraph talos["Talos / Kubernetes VMs"]
    cp["talos-cp-01<br/>control-plane<br/>192.168.1.178"]
    w1["talos-worker-01<br/>worker<br/>IP proposed: 192.168.1.179"]
    w2["talos-worker-02<br/>worker<br/>IP proposed: 192.168.1.180"]
  end

  subgraph k8s["homelab-talos Kubernetes"]
    pods["Pod CIDR<br/>10.42.0.0/16"]
    svcs["Service CIDR<br/>10.43.0.0/16"]
  end

  abundance --> vip
  elation --> vip
  remembrance --> vip
  vip --> mgmt
  mgmt --> vmnet
  abundance --> cp
  elation --> w1
  remembrance --> w2
  cp --> pods
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
- `the-abundance`, `the-elation`, and `the-remembrance` are intended to become the three physical Harvester nodes.
- The first Talos VM is active on `the-abundance`; one worker VM per remaining physical node is planned.
