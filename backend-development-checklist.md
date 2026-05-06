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

#### 2.1 Module Ownership And Dependency Direction

- Can a reviewer identify where transport, business logic, persistence, and external integrations live instead of finding those concerns mixed together without clear seams?
- Does the repository organize modules, packages, or directories so ownership and dependency direction are inspectable instead of hidden behind circular or cross-cutting imports?
- Are dependencies directed inward toward shared domain or application logic rather than allowing transport or infrastructure layers to own business rules by default?
- If multiple services, workers, or bounded contexts exist, does each one expose a clear ownership boundary instead of sharing mutable implementation details across unrelated areas?

#### 2.2 Contracts, Inputs, And Outputs

- Do API handlers, background jobs, event consumers, or command entry points define typed or otherwise explicit input and output contracts that a reviewer can inspect in code or schemas?
- Is input validation performed at the boundary where external data enters the backend instead of relying on downstream assumptions or ad hoc null checks?
- When the backend publishes or consumes versioned APIs, events, or job payloads, is compatibility strategy documented in code, schemas, or tests so a reviewer can see how breaking changes are controlled?
- Are error responses, domain failures, and retryable conditions represented through explicit contract shapes or conventions instead of inconsistent free-form strings?

#### 2.3 Code Quality Controls And Local Reasoning

- Does the repository define linting, formatting, or equivalent static checks that reviewers can run from the command line without editor-specific setup?
- Are naming, file placement, and exported interfaces consistent enough that a reviewer can predict where a new handler, service, repository, or adapter should live?
- Are side-effecting concerns such as filesystem access, network calls, environment lookup, time, or process execution isolated behind explicit boundaries a reviewer can trace?
- Does the code avoid hidden global state, mutable shared singletons, or magic configuration values that make runtime behavior difficult for a reviewer to follow?
- Are errors handled through explicit return paths, typed failures, or documented exception conventions instead of being silently swallowed or translated inconsistently across layers?

#### 2.4 Persistence, Dependencies, And Integration Seams

- Can a reviewer identify the modules responsible for database access, cache access, queue publishing, or third-party HTTP calls instead of finding those operations scattered through handlers or domain logic?
- Are persistence and network calls wrapped behind explicit repositories, gateways, clients, or adapters where a reviewer can inspect retry, timeout, and translation behavior?
- Does the backend keep data-access policy explicit, including transaction ownership, consistency expectations, and rules for cross-store or cross-service coordination where relevant?
- Are third-party libraries and generated clients introduced behind narrow seams so the backend can be tested, upgraded, or replaced without rewriting unrelated business logic?

### 3. Verification And Change Safety

#### 3.1 Test Evidence At The Correct Layer

- For each meaningful behavior change, can a reviewer identify direct test evidence at the correct layer, such as unit tests for pure logic, integration tests for persistence or integration seams, contract tests for schemas or interfaces, and end-to-end or smoke coverage where runtime wiring is the risk?
- Does the backend avoid relying on a single shallow test layer when the change crosses process, storage, queue, filesystem, or network boundaries that require stronger evidence?
- When a change affects public APIs, events, jobs, or commands, can a reviewer find verification that the observable contract still behaves as documented rather than only seeing internal helper tests?
- If a reviewer marks a lower test layer as sufficient, is the reason inspectable from the change scope and system boundary rather than implied by habit?

#### 3.2 Mocks, Fakes, And Real Dependency Coverage

- Are mocks, stubs, or fakes used to isolate pure decision logic or rare dependency conditions instead of replacing the exact dependency behavior that the change is supposed to prove?
- Where database queries, queue publishing, filesystem behavior, or outbound HTTP translation are part of the changed contract, can a reviewer find tests that exercise the real adapter, a production-like test harness, or another evidence source strong enough to verify integration correctness?
- When a fake or fixture replaces an external dependency, does it preserve the important contract shape, failure modes, and data semantics a reviewer would expect from production?
- Can a reviewer identify which dependencies are intentionally mocked and why, instead of inferring hidden gaps from test setup code?

#### 3.3 Determinism, Isolation, And Failure Cases

- Do tests control time, randomness, environment configuration, and external side effects well enough that repeated runs are deterministic and reviewer-reproducible?
- Are test fixtures, factories, or seed data scoped so one test does not rely on mutable state leaked from another test, process, or prior run?
- For the changed behavior, can a reviewer find explicit coverage for invalid input, dependency failure, and the user-visible or operator-visible outcome of those failures?
- When the backend implements retries, timeouts, cancellation, idempotency, or compensating behavior, do tests or equivalent evidence show both the success path and the failure or exhaustion path?

#### 3.4 Quality Gates And CI Readiness

- Does the repository document typecheck, lint, test, and any backend-specific verification commands in a form a reviewer can run locally without editor-specific setup?
- Are the same quality gates expected in CI, pre-merge automation, or another shared execution path instead of existing only as local tribal knowledge?
- If a backend does not support one of the standard gates such as typecheck or lint, is the substitute verification mechanism explicit enough that a reviewer can understand why the gap is acceptable?
- Can a reviewer determine from repository scripts, task runners, or CI configuration which commands are the source of truth for merge readiness?

### 4. Runtime And Operational Readiness

#### 4.1 Configuration And Secrets Handling

- Can a reviewer identify how the backend is configured across environments, including which settings are required at runtime and where secrets are expected to come from?
- Are secrets loaded from explicit secret-management or environment mechanisms instead of being hard-coded in source, fixtures, logs, or build artifacts?
- Does the backend validate required configuration at startup or deploy time so missing or malformed settings fail clearly instead of surfacing later as partial runtime behavior?
- Can a reviewer inspect which configuration values are safe defaults, which are environment-specific, and which are considered sensitive?

#### 4.2 Observability And Operator Signals

- Does the backend emit structured logs with enough context for a reviewer to verify request, job, or event outcomes without relying on free-form ad hoc strings?
- Are metrics, health surfaces, traces, or equivalent operational signals exposed for the critical runtime paths a reviewer would need to monitor?
- Where requests, jobs, or events cross process boundaries, can a reviewer identify correlation, trace, or request identifiers that support end-to-end debugging?
- Are errors reported with actionable context for operators, including the failing boundary or dependency, without exposing secrets or sensitive payloads?

#### 4.3 Deployment, Rollback, And Command Readiness

- Are deployment, rollback, or restart expectations documented well enough that a reviewer can verify how the service is expected to behave in production?
- Can a reviewer find the operational commands or automation used to start the backend, run migrations if applicable, execute smoke checks, and confirm readiness after deploy?
- If schema changes, background workers, or configuration rollouts require ordering constraints, is that sequencing explicit in repository docs, scripts, or release procedures?
- Does the backend define a safe rollback or forward-fix expectation that a reviewer can inspect when deploys partially fail?

#### 4.4 Background Jobs, Async Work, And Resilience

- For background jobs, scheduled tasks, or event consumers, can a reviewer identify ownership of retries, dead-letter handling, duplicate delivery, and failure visibility?
- Where async processing or external calls are used, are timeout, retry, and cancellation policies explicit in code or configuration instead of being left to library defaults?
- When an operation can be retried or delivered more than once, does the backend define idempotency or deduplication behavior that a reviewer can verify from contracts, storage rules, or tests?
- Does startup and shutdown behavior handle in-flight work safely, including readiness before serving traffic and graceful draining or cleanup when stopping?

### 5. Security And Dependency Hygiene

- Are authentication and authorization boundaries explicit at the transport or command boundary instead of being implied by downstream assumptions?
- Is untrusted input validated, normalized, and constrained before it reaches privileged operations, persistence, or external integrations?
- Does the backend avoid exposing secrets, access tokens, internal stack traces, or sensitive personal data in logs, error payloads, test fixtures, or generated artifacts?
- Are third-party dependencies, service credentials, and infrastructure permissions scoped to least privilege and kept narrow enough that a reviewer can inspect the blast radius?
- Can a reviewer identify how security-sensitive libraries, generated clients, or platform capabilities are introduced and upgraded without bypassing normal review or verification paths?

### 6. Sources

- `The Twelve-Factor App` informed configuration, environment separation, and deployability expectations so the checklist emphasizes explicit config and operational command surfaces.
- `OWASP API Security Top 10` informed the validation, authorization, and sensitive-data handling checks so the checklist covers baseline backend security review points.
- `Google SRE Workbook` informed observability, rollout safety, and operator-readiness expectations so runtime signals and deploy behavior stay reviewer-verifiable.
- `RFC 9110: HTTP Semantics` informed the contract and error-surface framing for APIs so status behavior and request handling expectations stay grounded in an external standard.
