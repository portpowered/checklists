from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKLIST_PATH = ROOT / "website-development-checklist.md"
EXAMPLE_PATH = ROOT / "examples" / "website-checklist-review-example.md"

REQUIRED_CHECKLIST_SNIPPETS = [
    "# Website Development Checklist (2026)",
    "## Purpose",
    "## How To Use This Checklist",
    "## Review Output Template",
    "## Status Definitions",
    "### 2.1 Build And Delivery Basics",
    "### 3.1 Accessibility",
    "### 3.2 Internationalization",
    "### 3.3 Performance",
    "### 3.4 Responsive Behavior",
    "### 3.5 SEO And Discoverability",
    "### 3.6 Security And Privacy",
    "### 4. Sources And Rationale",
]

REQUIRED_SOURCES = [
    "w3.org/TR/WCAG22",
    "developer.mozilla.org",
    "web.dev",
    "developers.google.com/search",
    "owasp.org",
]

REQUIRED_EXAMPLE_SNIPPETS = [
    "# Example Website Checklist Review",
    "## Review Record",
    "## Engineering Foundation Findings",
    "## Cross-Cutting Product Quality Findings",
    "## Outcome",
    "Pass",
    "Fail",
    "Needs Evidence",
    "Not Applicable",
]

REVIEW_RECORD_FIELDS = [
    "Project or repo",
    "Reviewer",
    "Review date",
    "Revision reviewed",
    "Evidence location",
    "Exceptions approved",
]


def read_text(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def lint_markdown_text(path: Path, text: str) -> None:
    require(text.endswith("\n"), f"{path.relative_to(ROOT)} must end with a newline")
    for number, line in enumerate(text.splitlines(), start=1):
        require("\t" not in line, f"{path.relative_to(ROOT)}:{number} contains a tab character")
        require(line == line.rstrip(), f"{path.relative_to(ROOT)}:{number} has trailing whitespace")


def lint_markdown(path: Path) -> None:
    lint_markdown_text(path, read_text(path))


def validate_example_text(text: str) -> None:
    for field in REVIEW_RECORD_FIELDS:
        require(
            f"| {field} |" in text,
            f"Example review is missing review-record field: {field}",
        )

    status_matches = re.findall(r"\|\s*(Pass|Fail|Needs Evidence|Not Applicable)\s*\|", text)
    require(status_matches, "Example review must include at least one recognized checklist status")
    for status in ("Pass", "Fail", "Needs Evidence", "Not Applicable"):
        require(
            status in status_matches,
            f"Example review must include a checklist row with status: {status}",
        )
    require(
        "### Evidence Notes" in text,
        "Example review must include evidence notes for reviewer-observable behavior",
    )


def typecheck_example() -> None:
    validate_example_text(read_text(EXAMPLE_PATH))


def validate_contract_text(checklist_text: str, example_text: str) -> None:
    validate_example_text(example_text)

    for snippet in REQUIRED_CHECKLIST_SNIPPETS:
        require(snippet in checklist_text, f"Checklist is missing required content: {snippet}")

    for source in REQUIRED_SOURCES:
        require(source in checklist_text, f"Checklist is missing required source reference: {source}")

    for snippet in REQUIRED_EXAMPLE_SNIPPETS:
        require(snippet in example_text, f"Example review is missing required content: {snippet}")

    require(
        "examples/website-checklist-review-example.md" in checklist_text,
        "Checklist must point reviewers to the completed example review artifact",
    )
    require(
        "2.1 Build And Delivery Basics" in example_text,
        "Example review must demonstrate engineering-foundation checklist usage",
    )
    require(
        "3.1 Accessibility" in example_text and "3.3 Performance" in example_text,
        "Example review must demonstrate cross-cutting checklist usage",
    )


def test_contract() -> None:
    validate_contract_text(read_text(CHECKLIST_PATH), read_text(EXAMPLE_PATH))


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in {"lint", "typecheck", "test"}:
        print("Usage: python scripts/validate_checklist.py [lint|typecheck|test]", file=sys.stderr)
        return 2

    command = argv[1]
    try:
        if command == "lint":
            lint_markdown(CHECKLIST_PATH)
            lint_markdown(EXAMPLE_PATH)
        elif command == "typecheck":
            typecheck_example()
        else:
            test_contract()
    except AssertionError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"{command} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
