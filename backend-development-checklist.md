# Backend Development Checklist (2026)

## Purpose

This checklist defines what a good backend looks like from the perspective of correctness, maintainability, and operational readiness. It is intended for implementation teams, reviewers, and technical leads who need a concrete pass/fail standard for planning, building, or auditing backend systems.

This document does not judge stylistic preference, personal code taste, or framework loyalty. Its primary concern is whether a backend is structured and reviewed in a way that is dependable, understandable, and reviewer-verifiable.

## How To Use This Checklist

Use this document during implementation planning, pull request review, release readiness review, and periodic technical audits.

- Mark each item as `Pass`, `Fail`, `Not Applicable`, or `Needs Evidence`.
- Only mark `Pass` when the reviewer can verify the claim by inspecting repository configuration, running documented project commands, or observing runtime behavior.
- Treat unchecked or unverifiable items as follow-up work rather than assumptions.
- Record links to evidence such as tests, CI jobs, dashboards, runbooks, logs, traces, or pull requests when a review requires traceability.
- Keep subjective code-style feedback separate from this checklist unless it affects correctness, maintainability, or operational readiness.

## Review Output Template

Use this template when applying the checklist to a specific project so the outcome is recorded consistently:

| Field | Required review content |
| --- | --- |
| Project or repo | Name of the backend or repository under review |
| Reviewer | Person performing the review |
| Review date | Date the checklist was applied |
| Revision reviewed | Commit SHA, release tag, or deployment identifier |
| Evidence location | Pull request, ticket, document, dashboard, or audit log that stores evidence |
| Exceptions approved | Explicit deviations that were accepted and by whom |

## Status Definitions

- `Pass`: The reviewer found direct evidence in the repository, CI, runtime behavior, or attached operational artifacts.
- `Fail`: The criterion is expected for this backend and the reviewer found contrary evidence or a missing implementation.
- `Needs Evidence`: The implementation may exist, but the reviewer cannot verify it from the available evidence.
- `Not Applicable`: The criterion does not apply to this backend, and the reason is documented in the review output.

## Review Rules

- Review the backend as a production system, not as an expression of personal coding taste.
- Prefer observable evidence over stated intent.
- Escalate exceptions explicitly when a product, regulatory, or infrastructure constraint justifies deviation.
- Keep architecture, testing, and runtime-readiness decisions tied to the evidence a reviewer can inspect.

## Checklist Sections

The sections below define the review surface for the full checklist. Every item is written so a reviewer can answer it from observable evidence instead of subjective preference.

### 1. Project Scope And Review Readiness

- Does the repository identify the backend's purpose, major responsibilities, and primary runtime boundaries?
- Can a reviewer find the commands or steps required to install dependencies, run the backend locally, execute automated checks, and produce a deployable build?
- Is there a documented place to record review evidence, exceptions, or follow-up work discovered during an audit?

### 2. Structure And Design Boundaries

- Can a reviewer identify where transport, business logic, persistence, and external integrations live instead of finding those concerns mixed together without clear seams?
- Does the repository organize modules, packages, or directories so ownership and dependency direction are inspectable instead of hidden behind circular or cross-cutting imports?
- Are side-effecting concerns such as filesystem access, network calls, environment lookup, time, or process execution isolated behind explicit boundaries a reviewer can trace?

### 3. Verification And Change Safety

- Does the backend expose documented quality gates such as typecheck, lint, test, or equivalent commands that reviewers can run without editor-specific setup?
- Can a reviewer identify test evidence for changed behavior instead of relying on comments or assumptions about correctness?
- Are failure paths, invalid input handling, and dependency errors represented in tests, runtime contracts, or review evidence where those risks matter?

### 4. Runtime And Operational Readiness

- Can a reviewer identify how the backend is configured across environments, including which settings are required at runtime and where secrets are expected to come from?
- Does the backend expose observable signals such as structured logs, health checks, metrics, traces, or actionable error reporting that support runtime debugging?
- Are deployment, rollback, or restart expectations documented well enough that a reviewer can verify how the service is expected to behave in production?

