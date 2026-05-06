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
- See `examples/website-checklist-review-example.md` for a completed sample review record that demonstrates the expected output shape and decision model.

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

#### 3.1 Accessibility

- Does the site target WCAG 2.2 Level AA as its baseline accessibility standard, with any exceptions documented explicitly in review evidence?
- Do pages use semantic HTML landmarks, heading structure, lists, tables, and button or link elements so a reviewer does not find custom widgets where native elements would satisfy the interaction?
- Can every interactive control be reached and operated with a keyboard alone without a keyboard trap?
- Is visible focus present on interactive elements, and does the focused element remain visible instead of being hidden under sticky headers, overlays, or clipped containers?
- Do form controls, icon-only buttons, dialogs, and custom widgets expose an accessible name, role, state, and error or help text that a reviewer can verify in the accessibility tree or with assistive technology?
- When the UI opens a modal, drawer, menu, route transition, or validation error state, is focus moved intentionally so keyboard and screen-reader users are not left behind?
- Are drag, swipe, or pointer-specific interactions backed by an alternative input path when the same task matters to core product use?
- Is important meaning conveyed without relying on color alone, and do text or control states preserve readable contrast in the shipped UI?
- Does the review evidence include both automated accessibility checks and manual verification such as keyboard traversal, screen-reader spot checks, or accessibility acceptance notes?

#### 3.2 Internationalization

- Does the root document set a valid `lang` value, and do localized content fragments override language where a reviewer can observe mixed-language content?
- When the product supports right-to-left languages or mixed-direction content, is direction handled semantically with HTML direction attributes where relevant instead of relying only on visual CSS overrides?
- Is user-facing copy externalized from component logic so a reviewer does not find hard-coded product strings scattered across implementation files?
- Are dates, times, numbers, currencies, lists, and relative-time values formatted through locale-aware APIs or framework helpers instead of manual string concatenation?
- Is locale selection, fallback behavior, and default-language behavior documented or implemented in a way a reviewer can verify from configuration or runtime behavior?
- Do layouts tolerate longer translated strings, alternate plural forms, and locale-dependent formatting without clipping, overlap, or hidden controls at supported breakpoints?

#### 3.3 Performance

- Does the project define a repeatable audit path for performance, such as Lighthouse, Lighthouse CI, PageSpeed Insights, or field telemetry, instead of relying on ad hoc browser impressions?
- If Core Web Vitals are measured, does the review evidence show LCP at or below 2.5 seconds, INP at or below 200 milliseconds, and CLS at or below 0.1 at the 75th percentile for the supported experience, or document why an exception is accepted?
- Are production JavaScript, CSS, font, and image assets fingerprinted or otherwise versioned so cache behavior can be verified across releases?
- Are non-critical images, embeds, and scripts deferred, lazy-loaded, or code-split where appropriate, while above-the-fold content needed for initial rendering is not delayed behind avoidable client-side work?
- Do images declare dimensions or equivalent reserved space so a reviewer can confirm that media loading does not introduce avoidable layout shifts?
- Is there a repository-level performance budget, CI assertion, or release gate that can detect regressions before deployment when the product depends on performance-sensitive flows?

#### 3.4 Responsive Behavior

- Does each user-facing page include a mobile viewport configuration appropriate for responsive rendering?
- Can the primary user journeys be completed at the supported mobile, tablet, and desktop widths without horizontal scrolling, clipped actions, or hidden essential content?
- Do layouts respond to available space with shared breakpoints or component rules that a reviewer can inspect instead of per-page one-off overrides?
- Do touch, mouse, and keyboard users all retain access to primary actions, without hover-only affordances hiding required functionality on coarse-pointer devices?
- Do responsive images, media, and embedded content scale within their containers without overflowing the viewport?

#### 3.5 SEO And Discoverability

- Does every indexable page expose a unique, accurate `<title>` and a meaningful meta description or equivalent metadata that matches the rendered content?
- Can search crawlers access the same important HTML, CSS, and JavaScript resources that normal users need to render the page, without those resources being blocked accidentally?
- If pages are meant to be indexed, are canonical URLs, crawl directives, and sitemap behavior configured intentionally rather than left ambiguous across environments?
- Is important content discoverable in rendered HTML so a reviewer does not find key page meaning hidden behind client-only rendering failures or blocked resources?
- When the content type benefits from it, is structured data present, valid, and tested with the relevant search tooling instead of being assumed correct?
- If a page or route should stay out of search results, is the exclusion mechanism explicit and documented so reviewers can distinguish intentional privacy from accidental invisibility?

#### 3.6 Security And Privacy

- Is the site served over HTTPS in production, with HTTP redirected or otherwise prevented where reviewers can verify transport security behavior?
- Are security headers configured intentionally for the rendered site, including a Content Security Policy and transport or embedding protections appropriate to the deployment?
- If the site uses cookies for sessions or authentication, are `Secure`, `HttpOnly`, and `SameSite` attributes set appropriately and observable in runtime responses?
- Are third-party scripts, tags, or embeds limited to justified use cases, with ownership and data purpose documented so reviewers can understand the privacy impact?
- Is user-generated or external input validated and output-encoded at the relevant boundaries so reviewers do not find raw untrusted HTML, script injection paths, or unsafe URL handling in normal flows?
- If the site collects analytics, marketing, or personal data, are consent, retention, and disclosure requirements implemented or documented in a way that can be reviewed from shipped behavior or repository configuration?

### 4. Sources And Rationale

The checklist above is informed by the following sources. Each source contributed concrete checks rather than general inspiration.

- W3C WCAG 2.2: establishes the accessibility conformance target and reinforced checks around keyboard operation, focus visibility, target size, redundant entry, and accessible authentication. Source: https://www.w3.org/TR/WCAG22/
- MDN HTML and Internationalization guidance: informed the checks for valid `lang` usage, semantic text direction with `dir`, and locale-aware formatting through the `Intl` APIs. Sources: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes , https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/dir , https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Internationalization
- Google web performance guidance on `web.dev` and Lighthouse: informed the Core Web Vitals thresholds, repeatable performance auditing, Lighthouse-based regression checks, and responsive viewport and layout expectations. Sources: https://web.dev/articles/vitals , https://web.dev/responsive-web-design-basics/ , https://web.dev/articles/lighthouse-ci , https://developer.chrome.com/docs/lighthouse/overview
- Google Search Central: informed the SEO and discoverability checks around rendered HTML, crawler access to CSS and JavaScript, structured data, and validation with Search Console tooling. Sources: https://developers.google.com/search/docs/fundamentals/seo-starter-guide , https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- OWASP Cheat Sheet Series: informed the security and privacy checks around HTTPS enforcement, Content Security Policy, HSTS, cookie attributes, and response-header hardening. Source: https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
