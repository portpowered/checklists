// @ts-check

import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";

import {
  CHECKLIST_FILE,
  readChecklist,
  validateChecklist
} from "../scripts/checklist-rules.mjs";

const VALID_CHECKLIST = `# Backend Development Checklist (2026)

## Purpose

This checklist defines what a good backend looks like from the perspective of correctness and operations.

## How To Use This Checklist

- Mark each item as Pass, Fail, Needs Evidence, or Not Applicable.

## Review Output Template

| Field | Required review content |
| --- | --- |
| Project or repo | Example backend |
| Reviewer | Example reviewer |
| Review date | 2026-05-06 |
| Revision reviewed | abc123 |
| Evidence location | CI job |
| Exceptions approved | None |

## Status Definitions

- Pass means the reviewer found direct evidence.

## Review Rules

- Prefer observable evidence over intent.

## Checklist Sections

### 1. Project Scope And Review Readiness

- Does the repository identify the backend's purpose and runtime boundaries?
- Can a reviewer find documented install, run, and build commands?
- Is there a documented place to record evidence and exceptions?

### 2. Structure And Design Boundaries

#### 2.1 Module Ownership And Dependency Direction

- Can a reviewer identify where transport, business logic, persistence, and integrations live?
- Does the repository organize modules so ownership and dependency direction are inspectable?
- Are dependencies directed inward toward shared domain or application logic?

#### 2.2 Contracts, Inputs, And Outputs

- Do handlers, jobs, or commands define explicit input and output contracts?
- Is input validation performed at the boundary where external data enters?
- Is compatibility strategy documented for versioned APIs, events, or payloads?

#### 2.3 Code Quality Controls And Local Reasoning

- Does the repository define linting and formatting checks that run from the command line?
- Are side-effecting concerns isolated behind explicit boundaries a reviewer can trace?
- Are errors handled through explicit return paths or documented exception conventions?

#### 2.4 Persistence, Dependencies, And Integration Seams

- Can a reviewer identify the modules responsible for database, cache, queue, or HTTP access?
- Are persistence and network calls wrapped behind explicit repositories, gateways, clients, or adapters?
- Are third-party libraries introduced behind narrow seams?

### 3. Verification And Change Safety

#### 3.1 Test Evidence At The Correct Layer

- Can a reviewer identify direct test evidence at the correct layer for each meaningful behavior change?
- Does the backend avoid relying on a single shallow test layer across risky boundaries?
- Can a reviewer verify public contract behavior rather than only helper internals?

#### 3.2 Mocks, Fakes, And Real Dependency Coverage

- Are mocks used to isolate decision logic instead of replacing the exact dependency behavior under proof?
- Can a reviewer find real adapter or production-like coverage where integration correctness matters?
- Can a reviewer identify which dependencies are intentionally mocked and why?

#### 3.3 Determinism, Isolation, And Failure Cases

- Do tests control time, randomness, environment, and side effects well enough to be deterministic?
- Are fixtures scoped so tests do not rely on leaked mutable state?
- Do tests cover invalid input, dependency failure, timeout exhaustion, and retry behavior?

#### 3.4 Quality Gates And CI Readiness

- Does the repository document typecheck, lint, and test commands a reviewer can run locally?
- Are the same quality gates expected in CI or another shared execution path?
- Can a reviewer determine which commands are the source of truth for merge readiness?

### 4. Runtime And Operational Readiness

#### 4.1 Configuration And Secrets Handling

- Can a reviewer identify how the backend is configured across environments?
- Are secrets loaded from explicit secret-management or environment mechanisms?
- Does the backend validate required configuration at startup?

#### 4.2 Observability And Operator Signals

- Does the backend emit structured logs with enough context for operators?
- Are metrics, health surfaces, or traces exposed for critical runtime paths?
- Can a reviewer identify correlation identifiers across process boundaries?

#### 4.3 Deployment, Rollback, And Command Readiness

- Are deployment, rollback, or restart expectations documented well enough for review?
- Can a reviewer find the commands used to start the backend and confirm readiness after deploy?
- Does the backend define a safe rollback or forward-fix expectation?

#### 4.4 Background Jobs, Async Work, And Resilience

- Can a reviewer identify retry, dead-letter, and failure visibility ownership for async work?
- Are timeout, retry, and cancellation policies explicit instead of left to library defaults?
- Does the backend define idempotency behavior for retried or duplicated operations?

### 5. Security And Dependency Hygiene

- Are authentication and authorization boundaries explicit at the transport or command boundary?
- Is untrusted input validated before it reaches privileged operations?
- Are third-party dependencies and credentials scoped to least privilege?

### 6. Sources

- The Twelve-Factor App informed configuration and deployability expectations.
- OWASP API Security Top 10 informed validation and authorization checks.
- Google SRE Workbook informed observability, rollout safety, and operator readiness.
- RFC 9110 informed contract and error-surface expectations.
`;

/**
 * @param {string} markdown
 * @returns {string}
 */
function createChecklistWorkspace(markdown) {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "backend-checklist-"));
  fs.writeFileSync(path.join(tempDir, CHECKLIST_FILE), markdown);
  return tempDir;
}

test("the repository ships a checklist artifact that satisfies the validator", () => {
  const checklist = readChecklist();
  assert.ok(checklist.includes("# Backend Development Checklist"), `${CHECKLIST_FILE} should start with the backend checklist title.`);
  assert.deepEqual(validateChecklist(checklist), []);
});

test("validateChecklist accepts a representative valid checklist", () => {
  assert.deepEqual(validateChecklist(VALID_CHECKLIST), []);
});

test("validateChecklist reports the exact rule failures for invalid checklist content", () => {
  const invalidChecklist = VALID_CHECKLIST
    .replace("## Review Rules", "## Review Guidance")
    .replace("- Are dependencies directed inward toward shared domain or application logic?", "- Are dependencies directed inward toward shared domain or application logic.")
    .replace("- RFC 9110 informed contract and error-surface expectations.", "- RFC 9110 covers HTTP semantics.");

  assert.deepEqual(validateChecklist(invalidChecklist), [
    'Missing required heading: "Review Rules".',
    'Checklist item must end with a question mark in "2.1 Module Ownership And Dependency Direction": - Are dependencies directed inward toward shared domain or application logic.',
    "Source entry must explain its contribution: - RFC 9110 covers HTTP semantics."
  ]);
});

test("lint-checklist CLI exits successfully for a valid checklist and fails for an invalid one", () => {
  const scriptPath = path.resolve("scripts/lint-checklist.mjs");
  const validWorkspace = createChecklistWorkspace(VALID_CHECKLIST);
  const invalidWorkspace = createChecklistWorkspace(VALID_CHECKLIST.replace("structured logs", "plain logs"));

  try {
    const validRun = spawnSync(process.execPath, [scriptPath], {
      cwd: validWorkspace,
      encoding: "utf8"
    });

    assert.equal(validRun.status, 0);
    assert.match(validRun.stdout, /Checklist lint passed\./);
    assert.equal(validRun.stderr, "");

    const invalidRun = spawnSync(process.execPath, [scriptPath], {
      cwd: invalidWorkspace,
      encoding: "utf8"
    });

    assert.equal(invalidRun.status, 1);
    assert.equal(invalidRun.stdout, "");
    assert.match(invalidRun.stderr, /Checklist must cover the term "structured logs"\./);
  } finally {
    fs.rmSync(validWorkspace, { recursive: true, force: true });
    fs.rmSync(invalidWorkspace, { recursive: true, force: true });
  }
});
