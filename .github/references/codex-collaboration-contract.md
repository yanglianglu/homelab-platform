# Codex Collaboration Contract

This repository uses a discuss-first workflow for homelab platform work.

Future Codex sessions must treat this as a standing contract, not a preference.

## Core Rule

Do not begin implementation just because an issue is next in Linear or the user
says to "proceed next".

The required flow is:

```text
Explain -> discuss options -> agree on approach -> implement -> verify -> update docs/Linear
```

## Before Implementation

Before editing files, changing cluster state, updating Linear issue state, or
making a durable product/tool decision, first explain:

- the issue goal
- the current context
- the options available
- the tradeoffs and risks
- the recommended path, clearly labeled as a recommendation
- the exact changes that would be made
- how success would be verified
- what would remain undone

Then ask for explicit approval to implement.

## What Counts As Implementation

Implementation includes:

- committing or pushing code
- editing repo docs or manifests
- applying Kubernetes resources
- changing Argo CD, External Secrets, Talos, Harvester, DNS, VPN, Gateway API,
  or legacy Ingress
- updating Linear status to In Progress, Done, or changing issue intent
- choosing a durable tool or product as platform policy
- creating or changing security/access/network policy

## What Is Allowed Before Approval

Read-only preparation is allowed:

- read Linear issues and comments
- inspect repository files
- run read-only cluster status commands
- summarize current state
- identify likely options and blockers
- draft a proposed plan for approval

## Ambiguous User Phrases

Interpret these as permission to explain and prepare, not as permission to
implement:

- "proceed next"
- "start the next issue"
- "what is next"
- "let's start"
- "continue"

After those phrases, explain the issue and ask for confirmation before making
durable changes.

## Why This Exists

The homelab is a learning platform and a durable infrastructure system. The
user needs the full picture before decisions become implementation. Codex should
help the user build understanding, not silently turn an issue into a product or
architecture choice.
