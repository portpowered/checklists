from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_checklist import (
    parse_checklist_questions,
    parse_findings_table,
    parse_required_review_template,
    parse_review_record,
    parse_status_definitions,
    validate_contract_text,
    validate_example_text,
)


VALID_CHECKLIST = """# Website Development Checklist (2026)

## Purpose

Checklist purpose.

## How To Use This Checklist

- See examples/website-checklist-review-example.md for a completed sample review record.
- See [examples/website-checklist-review-example.md](examples/website-checklist-review-example.md) for a completed sample review record.

## Review Output Template

| Field | Required review content |
| --- | --- |
| Project or repo | repo |
| Reviewer | reviewer |
| Review date | 2026-05-06 |
| Revision reviewed | abc1234 |
| Evidence location | PR #1 |
| Exceptions approved | none |

## Status Definitions

- `Pass`: direct evidence exists
- `Fail`: required behavior is missing
- `Needs Evidence`: evidence is incomplete
- `Not Applicable`: reason is documented

## Checklist Sections

#### 2.1 Build And Delivery Basics

- Does the repository expose reproducible install and build commands?

#### 2.2 Code Quality Controls

- Does CI run lint and type analysis before merge?

#### 2.3 State And Data Handling

- Can reviewers locate shared-state and server-state behavior?

#### 2.4 Styling System, Tailwind, And Design Tokens

- Are tokens defined in one inspectable source of truth?

#### 3.1 Accessibility

- Can keyboard users complete the primary interactions?

#### 3.2 Internationalization

- Are locale-sensitive values formatted with locale-aware APIs?

#### 3.3 Performance

- Does the project define a repeatable performance audit path?

#### 3.4 Responsive Behavior

- Can supported journeys complete at mobile, tablet, and desktop widths?

#### 3.5 SEO And Discoverability

- Do indexable pages expose intentional metadata and crawl behavior?

#### 3.6 Security And Privacy

- Are HTTPS, headers, and data-handling controls reviewable?

## 4. Sources And Rationale

- WCAG guidance for accessibility checks. Source: https://www.w3.org/TR/WCAG22/
- MDN guidance for semantic HTML and i18n checks. Source: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes
- web.dev guidance for performance checks. Source: https://web.dev/articles/vitals
- Google Search Central guidance for discoverability checks. Source: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- OWASP guidance for security checks. Source: https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
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
    def test_checklist_template_parses_required_fields(self) -> None:
        review_template = parse_required_review_template(VALID_CHECKLIST)
        self.assertEqual(review_template["Project or repo"], "repo")
        self.assertEqual(review_template["Evidence location"], "PR #1")

    def test_checklist_status_definitions_require_all_statuses(self) -> None:
        definitions = parse_status_definitions(VALID_CHECKLIST)
        self.assertEqual(definitions["Pass"], "direct evidence exists")
        self.assertEqual(definitions["Not Applicable"], "reason is documented")

    def test_checklist_questions_require_reviewer_verifiable_question_format(self) -> None:
        questions = parse_checklist_questions(VALID_CHECKLIST, "3.3 Performance")
        self.assertEqual(
            questions,
            ["Does the project define a repeatable performance audit path?"],
        )

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

    def test_contract_rejects_non_question_checklist_item(self) -> None:
        invalid_checklist = VALID_CHECKLIST.replace(
            "- Does the project define a repeatable performance audit path?\n",
            "- The project defines a repeatable performance audit path.\n",
        )

        with self.assertRaisesRegex(
            AssertionError,
            "Checklist subsection items must be reviewer-verifiable questions: 3.3 Performance",
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

    def test_test_command_reports_checklist_contract_failure(self) -> None:
        checklist = VALID_CHECKLIST.replace(
            "- Can keyboard users complete the primary interactions?\n",
            "- Keyboard support exists.\n",
        )

        result = run_validator_command("test", checklist_text=checklist)

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn(
            "ERROR: Checklist subsection items must be reviewer-verifiable questions: 3.1 Accessibility",
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
