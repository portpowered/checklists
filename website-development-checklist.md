# Website Development Checklist (2026)

## Purpose

This checklist defines what a good modern website looks like from an engineering, accessibility, performance, and maintainability perspective. It is intended for implementation teams, reviewers, and technical leads who need a concrete pass/fail standard for planning, building, or auditing a website.

This document does not judge aesthetic taste, brand style, or visual trend alignment. Its primary concern is whether a website is built and operated in a way that is reliable, accessible, maintainable, and reviewer-verifiable.

## How To Use This Checklist

Use this document during implementation planning, pull request review, release readiness review, and periodic technical audits.

- Mark each item as `Pass`, `Fail`, `Not Applicable`, or `Needs Evidence`.
- Only mark `Pass` when the reviewer can verify the claim by inspecting repository configuration, running project commands, or observing runtime behavior.
- Treat unchecked or unverifiable items as follow-up work rather than assumptions.
- Record links to evidence such as scripts, config files, CI jobs, screenshots, audits, or live behavior when a review requires traceability.

## Review Output Template

Use this template when applying the checklist to a specific project so the outcome is recorded consistently:

| Field | Required review content |
| --- | --- |
| Project or repo | Name of the website or repository under review |
| Reviewer | Person performing the review |
| Review date | Date the checklist was applied |
| Revision reviewed | Commit SHA, release tag, or deployment identifier |
| Evidence location | Pull request, ticket, document, or audit log that stores evidence |
| Exceptions approved | Explicit deviations that were accepted and by whom |

## Status Definitions

- `Pass`: The reviewer found direct evidence in the repository, CI, deployed behavior, or an attached audit artifact.
- `Fail`: The criterion is expected for this project and the reviewer found contrary evidence or a missing implementation.
- `Needs Evidence`: The implementation may exist, but the reviewer cannot verify it from the available evidence.
- `Not Applicable`: The criterion does not apply to this project, and the reason is documented in the review output.

## Review Rules

- Review the website as an engineering system, not as a visual mood board.
- Prefer observable evidence over stated intent.
- Escalate exceptions explicitly when a product, regulatory, or platform constraint justifies deviation.
- Keep design-taste feedback separate from this checklist unless the item affects usability, accessibility, or maintainability.

## Checklist Sections

The sections below define the review surface for the full checklist. Every item is written so a reviewer can answer it from observable evidence instead of subjective taste.

### 1. Project Scope And Review Readiness

- Does the repository identify the website's intended audience, supported environments, and primary delivery path?
- Can a reviewer find the commands or steps required to install dependencies, run the site locally, and produce a production build?
- Is there a documented place to record review evidence, exceptions, or follow-up work discovered during an audit?

### 2. Engineering Foundation

#### 2.1 Build And Delivery Basics

- Is dependency installation pinned by a committed lockfile so a reviewer can reproduce the dependency graph from a clean checkout?
- Does the repository expose a documented local development command that starts the website with the same framework and major configuration used in normal development?
- Does the repository expose a documented production build command that succeeds without manual file edits or hidden machine-local prerequisites?
- Can CI run the same install, lint, test, and build commands that developers use locally without requiring interactive prompts?
- Does the production build output come from source-controlled configuration rather than undocumented ad hoc shell steps?
- Are environment variables or secrets required for build and deployment documented by name, purpose, and expected source?
- Does the deployment path define cache-busting or asset fingerprinting behavior so a reviewer can confirm static assets are versioned for release?

#### 2.2 Code Quality Controls

- Does the repository define a lint command that runs without opening an editor and fails the build on rule violations?
- Does the repository define a formatting expectation through a formatter configuration, lint rule set, or documented command that reviewers can run consistently?
- Is TypeScript configured in strict mode, or is every disabled strictness option explicitly justified in repository configuration?
- Are TypeScript escape hatches such as `any`, `@ts-ignore`, or unchecked type assertions rare enough that a reviewer can find and justify each remaining use?
- Do React components follow the framework's current rendering and data-flow model without relying on legacy class components or deprecated lifecycle patterns unless the repository documents an exception?
- Are shared UI primitives, hooks, and utility modules organized so a reviewer can trace where business logic lives instead of finding it duplicated across unrelated components?
- Does CI or a pre-merge check run the repository's static analysis commands before code is considered releasable?

#### 2.3 State And Data Handling

- Is local component state used for view-local concerns such as toggles, form drafts, and transient UI status instead of promoting that state into a global store without evidence of reuse?
- When multiple routes or distant components share client state, does the repository use an explicit shared-state mechanism rather than prop drilling through unrelated layers?
- When server data is cached on the client, does the repository use a dedicated server-state pattern or library that exposes loading, error, refresh, and invalidation behavior?
- Can a reviewer identify where network requests, cache updates, optimistic updates, and retry behavior are implemented instead of finding them embedded inconsistently across UI components?
- Are form submissions and mutations designed so success, pending, validation-error, and failure states are observable in the UI or test suite?
- Does the code avoid storing duplicated derived state when the same value can be recomputed from a smaller source of truth?

#### 2.4 Styling System, Tailwind, And Design Tokens

- If Tailwind is part of the stack, is it configured centrally and used through shared utility conventions rather than arbitrary one-off local build setups?
- Does the repository define design tokens for core values such as color, spacing, typography, radius, elevation, or motion instead of scattering raw values across components?
- Are tokens expressed in a reusable source of truth such as CSS custom properties, Tailwind theme configuration, or a dedicated token file that reviewers can inspect?
- Do components consume tokenized values through approved abstractions rather than repeatedly hard-coding hex colors, pixel values, or breakpoint numbers inline?
- Are responsive breakpoints defined in one inspectable configuration layer so reviewers can verify that layout behavior is consistent across the site?
- Is there a documented policy for component variants, composition, or shared patterns so styling decisions remain maintainable as the UI surface grows?
- If custom CSS exists alongside Tailwind utilities, is its purpose constrained to tokens, resets, rich content styling, or cases where utilities alone would reduce clarity?

### 3. Cross-Cutting Product Quality

- Can a reviewer inspect a dedicated section for accessibility, internationalization, performance, responsive behavior, SEO or discoverability, and security or privacy?
- Are cross-cutting quality requirements written so they can be verified by browser behavior, metadata, automated audits, or production configuration?

### 4. Sources And Rationale

- Does the final checklist include a small set of authoritative external sources that explain where the review standard came from?
- Does each source contribute to concrete checklist expectations instead of serving as general reading material?
