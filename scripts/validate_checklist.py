from __future__ import annotations

import re
import sys
import os
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parent.parent
ALLOWED_STATUSES = {"Pass", "Fail", "Needs Evidence", "Not Applicable"}
REQUIRED_ENGINEERING_SECTIONS = {
    "2.1 Build And Delivery Basics",
    "2.2 Code Quality Controls",
    "2.3 State And Data Handling",
    "2.4 Styling System, Tailwind, And Design Tokens",
}
REQUIRED_CROSS_CUTTING_SECTIONS = {
    "3.1 Accessibility",
    "3.2 Internationalization",
    "3.3 Performance",
    "3.4 Responsive Behavior",
    "3.5 SEO And Discoverability",
    "3.6 Security And Privacy",
}

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
        raise AssertionError(f"Missing required file: {display_path(path)}")
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def get_root() -> Path:
    return Path(os.environ.get("CHECKLIST_VALIDATOR_ROOT", DEFAULT_ROOT)).resolve()


def get_checklist_path() -> Path:
    configured = os.environ.get("CHECKLIST_PATH")
    if configured:
        return Path(configured).resolve()
    return get_root() / "website-development-checklist.md"


def get_example_path() -> Path:
    configured = os.environ.get("EXAMPLE_PATH")
    if configured:
        return Path(configured).resolve()
    return get_root() / "examples" / "website-checklist-review-example.md"


def display_path(path: Path) -> str:
    root = get_root()
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def extract_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"(?ms)^## {re.escape(heading)}\n(.*?)(?=^## |\Z)",
    )
    match = pattern.search(text)
    require(match is not None, f"Missing required section: ## {heading}")
    return match.group(1).strip()


def parse_markdown_table(section_text: str) -> list[dict[str, str]]:
    lines = [line.strip() for line in section_text.splitlines() if line.strip()]
    table_lines = [line for line in lines if line.startswith("|") and line.endswith("|")]
    require(len(table_lines) >= 2, "Expected a markdown table with a header and separator")

    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    separator_cells = [cell.strip() for cell in table_lines[1].strip("|").split("|")]
    require(
        len(headers) == len(separator_cells),
        "Markdown table separator must match the header column count",
    )
    require(
        all(set(cell) <= {"-", ":"} and cell for cell in separator_cells),
        "Markdown table must include a valid separator row",
    )

    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        require(
            len(cells) == len(headers),
            "Markdown table row column count does not match the header",
        )
        rows.append(dict(zip(headers, cells)))
    require(rows, "Markdown table must include at least one data row")
    return rows


def parse_review_record(text: str) -> dict[str, str]:
    section_text = extract_section(text, "Review Record")
    rows = parse_markdown_table(section_text)
    fields = {row["Field"]: row["Example review content"] for row in rows}

    for field in REVIEW_RECORD_FIELDS:
        require(field in fields, f"Example review is missing review-record field: {field}")
        require(fields[field], f"Example review field must not be empty: {field}")
    return fields


def parse_findings_table(text: str, heading: str, expected_sections: set[str]) -> list[dict[str, str]]:
    section_text = extract_section(text, heading)
    rows = parse_markdown_table(section_text)
    seen_sections = set()

    for row in rows:
        section_name = row["Checklist section"]
        status = row["Status"]
        evidence = row["Evidence summary"]
        require(
            section_name in expected_sections,
            f"{heading} contains an unexpected checklist section: {section_name}",
        )
        require(section_name not in seen_sections, f"{heading} repeats checklist section: {section_name}")
        seen_sections.add(section_name)
        require(status in ALLOWED_STATUSES, f"{heading} contains an invalid status: {status}")
        require(evidence, f"{heading} must include evidence for section: {section_name}")

    missing_sections = expected_sections - seen_sections
    require(
        not missing_sections,
        f"{heading} is missing checklist sections: {', '.join(sorted(missing_sections))}",
    )
    return rows


def lint_markdown_text(path: Path, text: str) -> None:
    require(text.endswith("\n"), f"{display_path(path)} must end with a newline")
    for number, line in enumerate(text.splitlines(), start=1):
        require("\t" not in line, f"{display_path(path)}:{number} contains a tab character")
        require(line == line.rstrip(), f"{display_path(path)}:{number} has trailing whitespace")


def lint_markdown(path: Path) -> None:
    lint_markdown_text(path, read_text(path))


def validate_example_text(text: str) -> None:
    parse_review_record(text)
    engineering_rows = parse_findings_table(
        text,
        "Engineering Foundation Findings",
        REQUIRED_ENGINEERING_SECTIONS,
    )
    cross_cutting_rows = parse_findings_table(
        text,
        "Cross-Cutting Product Quality Findings",
        REQUIRED_CROSS_CUTTING_SECTIONS,
    )

    status_matches = [row["Status"] for row in engineering_rows + cross_cutting_rows]
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
    validate_example_text(read_text(get_example_path()))


def validate_contract_text(checklist_text: str, example_text: str) -> None:
    validate_example_text(example_text)

    for snippet in REQUIRED_CHECKLIST_SNIPPETS:
        require(snippet in checklist_text, f"Checklist is missing required content: {snippet}")

    for source in REQUIRED_SOURCES:
        require(source in checklist_text, f"Checklist is missing required source reference: {source}")

    for snippet in REQUIRED_EXAMPLE_SNIPPETS:
        require(snippet in example_text, f"Example review is missing required content: {snippet}")

    link_match = re.search(
        r"\[examples/website-checklist-review-example\.md\]\(([^)]+)\)",
        checklist_text,
    )
    require(
        link_match is not None,
        "Checklist must point reviewers to the completed example review artifact",
    )
    require(
        link_match.group(1) == "examples/website-checklist-review-example.md",
        "Checklist example-review link must use a repository-relative markdown target",
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
    validate_contract_text(read_text(get_checklist_path()), read_text(get_example_path()))


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in {"lint", "typecheck", "test"}:
        print("Usage: python scripts/validate_checklist.py [lint|typecheck|test]", file=sys.stderr)
        return 2

    command = argv[1]
    try:
        if command == "lint":
            lint_markdown(get_checklist_path())
            lint_markdown(get_example_path())
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
