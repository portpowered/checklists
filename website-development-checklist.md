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

## Review Rules

- Review the website as an engineering system, not as a visual mood board.
- Prefer observable evidence over stated intent.
- Escalate exceptions explicitly when a product, regulatory, or platform constraint justifies deviation.
- Keep design-taste feedback separate from this checklist unless the item affects usability, accessibility, or maintainability.

## Checklist Sections

The sections below define the review surface for the full checklist. Each section will be expanded with concrete pass/fail checks and supporting source references.

### 1. Project Scope And Review Readiness

- Does the repository identify the website's intended audience, supported environments, and primary delivery path?
- Can a reviewer find the commands or steps required to install dependencies, run the site locally, and produce a production build?
- Is there a documented place to record review evidence, exceptions, or follow-up work discovered during an audit?

### 2. Engineering Foundation

- Can a reviewer inspect a dedicated section for build tooling, scripts, code quality controls, TypeScript expectations, React usage, state handling, Tailwind usage, and design-token strategy?
- Are foundation requirements written so they can be verified from repository files, CI configuration, or application behavior instead of subjective preference?

### 3. Cross-Cutting Product Quality

- Can a reviewer inspect a dedicated section for accessibility, internationalization, performance, responsive behavior, SEO or discoverability, and security or privacy?
- Are cross-cutting quality requirements written so they can be verified by browser behavior, metadata, automated audits, or production configuration?

### 4. Sources And Rationale

- Does the final checklist include a small set of authoritative external sources that explain where the review standard came from?
- Does each source contribute to concrete checklist expectations instead of serving as general reading material?

