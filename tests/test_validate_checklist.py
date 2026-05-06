from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_checklist import parse_findings_table, parse_review_record, validate_contract_text, validate_example_text


VALID_CHECKLIST = """# Website Development Checklist (2026)

## Purpose

Checklist purpose.

## How To Use This Checklist

- See examples/website-checklist-review-example.md for a completed sample review record.
- See [examples/website-checklist-review-example.md](examples/website-checklist-review-example.md) for a completed sample review record.

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
| 2.2 Code Quality Controls | Pass | ci output shows lint and typecheck |
| 2.3 State And Data Handling | Needs Evidence | cache invalidation behavior is not documented |
| 2.4 Styling System, Tailwind, And Design Tokens | Pass | shared tokens drive spacing and color decisions |

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
    def test_review_record_parses_required_fields(self) -> None:
        review_record = parse_review_record(VALID_EXAMPLE)
        self.assertEqual(review_record["Project or repo"], "example")
        self.assertEqual(review_record["Reviewer"], "reviewer")

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

    def test_example_rejects_missing_findings_evidence(self) -> None:
        invalid_example = VALID_EXAMPLE.replace(
            "| 3.3 Performance | Pass | lighthouse report attached |\n",
            "| 3.3 Performance | Pass |  |\n",
        )

        with self.assertRaisesRegex(
            AssertionError,
            "Cross-Cutting Product Quality Findings must include evidence for section: 3.3 Performance",
        ):
            validate_example_text(invalid_example)

    def test_findings_parser_rejects_unknown_sections(self) -> None:
        findings_text = """| Checklist section | Status | Evidence summary |
| --- | --- | --- |
| 9.9 Imaginary Section | Pass | evidence |
"""

        with self.assertRaisesRegex(
            AssertionError,
            "Engineering Foundation Findings contains an unexpected checklist section: 9.9 Imaginary Section",
        ):
            parse_findings_table(
                f"## Engineering Foundation Findings\n\n{findings_text}\n",
                "Engineering Foundation Findings",
                {
                    "2.1 Build And Delivery Basics",
                },
            )

    def test_contract_rejects_non_relative_example_link(self) -> None:
        invalid_checklist = VALID_CHECKLIST.replace(
            "(examples/website-checklist-review-example.md)",
            "(/C:/Users/example/website-checklist-review-example.md)",
        )

        with self.assertRaisesRegex(
            AssertionError,
            "Checklist example-review link must use a repository-relative markdown target",
        ):
            validate_contract_text(invalid_checklist, VALID_EXAMPLE)


class ValidateChecklistCliTests(unittest.TestCase):
    def test_lint_command_reports_success(self) -> None:
        result = run_validator_command("lint")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "lint passed")
        self.assertEqual(result.stderr, "")

    def test_lint_command_reports_failure_details(self) -> None:
        checklist = VALID_CHECKLIST.rstrip("\n")

        result = run_validator_command("lint", checklist_text=checklist)

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("ERROR: website-development-checklist.md must end with a newline", result.stderr)

    def test_typecheck_command_reports_success(self) -> None:
        result = run_validator_command("typecheck")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "typecheck passed")
        self.assertEqual(result.stderr, "")

    def test_typecheck_command_reports_review_record_failure(self) -> None:
        example = VALID_EXAMPLE.replace(
            "| Reviewer | reviewer |\n",
            "",
        )

        result = run_validator_command("typecheck", example_text=example)

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("ERROR: Example review is missing review-record field: Reviewer", result.stderr)

    def test_test_command_reports_contract_failure(self) -> None:
        checklist = VALID_CHECKLIST.replace(
            "(examples/website-checklist-review-example.md)",
            "(/tmp/non-relative-link.md)",
        )

        result = run_validator_command("test", checklist_text=checklist)

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn(
            "ERROR: Checklist example-review link must use a repository-relative markdown target",
            result.stderr,
        )


def run_validator_command(
    command: str,
    *,
    checklist_text: str = VALID_CHECKLIST,
    example_text: str = VALID_EXAMPLE,
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        example_dir = root / "examples"
        example_dir.mkdir()
        (root / "website-development-checklist.md").write_text(checklist_text, encoding="utf-8")
        (example_dir / "website-checklist-review-example.md").write_text(example_text, encoding="utf-8")

        env = os.environ.copy()
        env["CHECKLIST_VALIDATOR_ROOT"] = str(root)

        return subprocess.run(
            [sys.executable, "scripts/validate_checklist.py", command],
            capture_output=True,
            text=True,
            env=env,
            cwd=Path(__file__).resolve().parent.parent,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
