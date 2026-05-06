# Example Website Checklist Review

This example shows how a reviewer can apply `website-development-checklist.md` to a concrete repository review and produce an evidence-backed pass/fail record.

## Review Record

| Field | Example review content |
| --- | --- |
| Project or repo | `acme-marketing-site` |
| Reviewer | `Taylor Reviewer` |
| Review date | `2026-05-06` |
| Revision reviewed | `abc1234` |
| Evidence location | `PR #42`, Lighthouse report, accessibility notes |
| Exceptions approved | `Not Applicable` for right-to-left layout support because the product ships English-only content today |

## Engineering Foundation Findings

| Checklist section | Status | Evidence summary |
| --- | --- | --- |
| 2.1 Build And Delivery Basics | Pass | `pnpm install`, `pnpm dev`, and `pnpm build` are documented in the repo and mirrored by CI. |
| 2.2 Code Quality Controls | Pass | CI runs lint and TypeScript checks, and the repository keeps strict mode enabled in `tsconfig.json`. |
| 2.3 State And Data Handling | Needs Evidence | The reviewer found data fetching hooks, but retry and cache invalidation behavior were not documented in the pull request evidence. |
| 2.4 Styling System, Tailwind, And Design Tokens | Pass | Colors, spacing, and typography are defined through shared CSS custom properties and Tailwind theme tokens. |

## Cross-Cutting Product Quality Findings

| Checklist section | Status | Evidence summary |
| --- | --- | --- |
| 3.1 Accessibility | Pass | Keyboard traversal, visible focus, accessible labels, and dialog focus management were verified manually and with automated checks. |
| 3.2 Internationalization | Fail | User-facing date strings are still manually concatenated in one checkout component instead of using locale-aware formatting. |
| 3.3 Performance | Pass | Lighthouse CI and production telemetry both show the primary route within the team's Core Web Vitals targets. |
| 3.4 Responsive Behavior | Pass | Primary flows were verified at mobile, tablet, and desktop widths without horizontal overflow. |
| 3.5 SEO And Discoverability | Pass | The page exposes a unique title, canonical URL, and crawlable rendered HTML. |
| 3.6 Security And Privacy | Needs Evidence | CSP ownership and cookie attribute verification were not attached to the release evidence. |

## Outcome

- Pass criteria can be defended with repository or runtime evidence.
- Fail criteria become tracked follow-up work instead of remaining implicit.
- Needs Evidence remains distinct from Fail so reviewers do not overstate what they actually verified.
- Not Applicable is only valid when the reason is captured in the review record.

### Evidence Notes

- This example demonstrates that a reviewer can complete a concrete audit record directly from the checklist structure.
- The mixed `Pass`, `Fail`, `Needs Evidence`, and `Not Applicable` outcomes show the intended decision model rather than a documentation-only outline.
