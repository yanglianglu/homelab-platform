# Execution Plan Template

Use this template for non-trivial, ambiguous, or operationally risky work.

## Objective

What outcome should exist when this gate is done?

## Current State

What is known now? Include repo paths, live-state summary if applicable, and unknowns.

## Target State

What should be true after the work?

## Scope

What will change in this gate?

## Out of Scope

What will not change in this gate?

## Assumptions

What must be true for the plan to be safe?

## Risks

What can fail, what is the blast radius, and what signals indicate trouble?

## Steps

1. Inspect current state.
2. Make the smallest useful change.
3. Validate locally or with dry-run.
4. Stop at the next gate unless live approval is explicit.

## Validation

What commands, renders, health checks, or reviews prove the gate worked?

## Rollback

How will the change be reverted or recovered?

## Stop Conditions

When should Codex stop and ask before continuing?

## Final Report Format

- Result
- Files changed
- Commands run
- Validation
- Risks and assumptions
- Next gate
