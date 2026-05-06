from __future__ import annotations

import unittest

from scripts.validate_checklist import validate_contract_text, validate_example_text


VALID_CHECKLIST = """# Website Development Checklist (2026)

## Purpose

Checklist purpose.

## How To Use This Checklist

- See examples/website-checklist-review-example.md for a completed sample review record.

## Review Output Template

## Status Definitions

### 2.1 Build And Delivery Basics

### 3.1 Accessibility

### 3.2 Internationalization

### 3.3 Performance

### 3.4 Responsive Behavior

### 3.5 SEO And Discoverability

### 3.6 Security And Privacy

### 4. Sources And Rationale

https://www.w3.org/TR/WCAG22/
https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes
https://web.dev/articles/vitals
https://developers.google.com/search/docs/fundamentals/seo-starter-guide
https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
"""

VALID_EXAMPLE = """# Example Website Checklist Review

## Review Record

| Field | Example review content |
| --- | --- |
| Project or repo | example |
| Reviewer | reviewer |
| Review date | 2026-05-06 |
| Revision reviewed | abc1234 |
| Evidence location | PR #1 |
| Exceptions approved | noindex for private routes |

## Engineering Foundation Findings

| Checklist section | Status | Evidence summary |
| --- | --- | --- |
| 2.1 Build And Delivery Basics | Pass | build docs exist |
| 2.2 Code Quality Controls | Needs Evidence | ci output missing |

## Cross-Cutting Product Quality Findings

| Checklist section | Status | Evidence summary |
| --- | --- | --- |
| 3.1 Accessibility | Pass | manual and automated checks passed |
| 3.2 Internationalization | Fail | locale formatting is manual |
| 3.3 Performance | Pass | lighthouse report attached |
| 3.4 Responsive Behavior | Pass | verified at supported widths |
| 3.5 SEO And Discoverability | Not Applicable | authenticated noindex portal |
| 3.6 Security And Privacy | Needs Evidence | cookie evidence missing |

## Outcome

### Evidence Notes

- The review record demonstrates all four statuses.
"""


class ValidateChecklistTests(unittest.TestCase):
    def test_example_accepts_all_required_statuses(self) -> None:
        validate_example_text(VALID_EXAMPLE)

    def test_example_rejects_missing_not_applicable_row(self) -> None:
        invalid_example = VALID_EXAMPLE.replace(
            "| 3.5 SEO And Discoverability | Not Applicable | authenticated noindex portal |\n",
            "| 3.5 SEO And Discoverability | Pass | public pages have titles |\n",
        )

        with self.assertRaisesRegex(
            AssertionError,
            "Example review must include a checklist row with status: Not Applicable",
        ):
            validate_example_text(invalid_example)

    def test_contract_rejects_missing_example_link(self) -> None:
        invalid_checklist = VALID_CHECKLIST.replace(
            "examples/website-checklist-review-example.md",
            "examples/missing.md",
        )

        with self.assertRaisesRegex(
            AssertionError,
            "Checklist must point reviewers to the completed example review artifact",
        ):
            validate_contract_text(invalid_checklist, VALID_EXAMPLE)


if __name__ == "__main__":
    unittest.main()
