# Checklist README

This repository contains checklist artifacts and a minimal factory setup for processing `task` work items.

## Project Checklist

- [ ] Review [`factory/factory.json`](factory/factory.json) to confirm the workflow matches your intent.
- [ ] Add incoming task files under [`factory/inputs/README.md`](factory/inputs/README.md)'s starter inbox path: `inputs/task/default/`.
- [ ] Update the worker definition in [`factory/workers/processor/AGENTS.md`](factory/workers/processor/AGENTS.md) if the processor needs different instructions, tools, or timeout settings.
- [ ] Update the workstation prompt in [`factory/workstations/process/AGENTS.md`](factory/workstations/process/AGENTS.md) if each work item needs additional context or formatting rules.
- [ ] Confirm the `task` lifecycle states are correct: `init`, `complete`, and `failed`.
- [ ] Confirm the `process` workstation should route `task/init` work to the `processor` worker.
- [ ] Start the local factory runtime that consumes the starter inbox and executes work items.
- [ ] Submit a test task and verify it moves from `init` to `complete`.
- [ ] Inspect failure handling and confirm failed work lands in the `failed` state as expected.
- [ ] Replace this checklist with team-specific operating notes if this repository becomes a long-lived project.

## Current Flow

1. A `task` work item is submitted to the starter inbox.
2. The `process` workstation picks up `task` items in the `init` state.
3. The `processor` worker handles the request.
4. Successful work exits as `complete`; failures exit as `failed`.

## Checklist Quality Commands

- `make lint` validates markdown hygiene for the checklist deliverables in this repository.
- `make typecheck` validates the completed example review record against the required review fields and status model.
- `make test` runs CLI-level validator tests against isolated fixtures and then validates the checked-in checklist review contract.
