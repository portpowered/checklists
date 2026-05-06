// @ts-check

import fs from "node:fs";
import path from "node:path";

/**
 * @typedef {{ level: number, title: string, line: number }} Heading
 * @typedef {{ title: string, level: number, body: string }} Section
 */

export const CHECKLIST_FILE = "backend-development-checklist.md";

export const REQUIRED_HEADINGS = [
  "Purpose",
  "How To Use This Checklist",
  "Review Output Template",
  "Status Definitions",
  "Review Rules",
  "Checklist Sections",
  "1. Project Scope And Review Readiness",
  "2. Structure And Design Boundaries",
  "2.1 Module Ownership And Dependency Direction",
  "2.2 Contracts, Inputs, And Outputs",
  "2.3 Code Quality Controls And Local Reasoning",
  "2.4 Persistence, Dependencies, And Integration Seams",
  "3. Verification And Change Safety",
  "3.1 Test Evidence At The Correct Layer",
  "3.2 Mocks, Fakes, And Real Dependency Coverage",
  "3.3 Determinism, Isolation, And Failure Cases",
  "3.4 Quality Gates And CI Readiness",
  "4. Runtime And Operational Readiness",
  "4.1 Configuration And Secrets Handling",
  "4.2 Observability And Operator Signals",
  "4.3 Deployment, Rollback, And Command Readiness",
  "4.4 Background Jobs, Async Work, And Resilience",
  "5. Security And Dependency Hygiene",
  "6. Sources"
];

export const REQUIRED_REVIEW_FIELDS = [
  "Project or repo",
  "Reviewer",
  "Review date",
  "Revision reviewed",
  "Evidence location",
  "Exceptions approved"
];

/**
 * @param {string} repoRoot
 */
export function readChecklist(repoRoot = process.cwd()) {
  return fs.readFileSync(path.join(repoRoot, CHECKLIST_FILE), "utf8");
}

/**
 * @param {string} markdown
 * @returns {Heading[]}
 */
export function parseHeadings(markdown) {
  return markdown
    .split(/\r?\n/)
    .flatMap((line, index) => {
      const match = /^(#{2,4})\s+(.*)$/.exec(line);
      if (!match) {
        return [];
      }

      return [{
        level: match[1].length,
        title: match[2].trim(),
        line: index + 1
      }];
    });
}

/**
 * @param {string} markdown
 * @returns {Section[]}
 */
export function extractSections(markdown) {
  const headings = parseHeadings(markdown);
  const lines = markdown.split(/\r?\n/);

  return headings.map((heading, index) => {
    const start = heading.line;
    let end = lines.length;

    for (let i = index + 1; i < headings.length; i += 1) {
      if (headings[i].level <= heading.level) {
        end = headings[i].line - 1;
        break;
      }
    }

    return {
      title: heading.title,
      level: heading.level,
      body: lines.slice(start, end).join("\n").trim()
    };
  });
}

/**
 * @param {Section[]} sections
 * @param {string} title
 * @returns {Section | undefined}
 */
export function findSection(sections, title) {
  return sections.find((section) => section.title === title);
}

/**
 * @param {string} text
 * @returns {string[]}
 */
export function bulletLines(text) {
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.startsWith("- "));
}

/**
 * @param {string} markdown
 * @returns {string[]}
 */
export function validateChecklist(markdown) {
  /** @type {string[]} */
  const errors = [];
  const sections = extractSections(markdown);
  const headings = new Set(sections.map((section) => section.title));

  for (const heading of REQUIRED_HEADINGS) {
    if (!headings.has(heading)) {
      errors.push(`Missing required heading: "${heading}".`);
    }
  }

  const reviewTemplate = findSection(sections, "Review Output Template");
  if (!reviewTemplate) {
    errors.push("Missing review output template section.");
  } else {
    for (const field of REQUIRED_REVIEW_FIELDS) {
      if (!reviewTemplate.body.includes(field)) {
        errors.push(`Review output template is missing the "${field}" field.`);
      }
    }
  }

  for (const section of sections) {
    const numberedChecklistSection = /^[1-5](\.\d+)? /.test(section.title);
    if (!numberedChecklistSection) {
      continue;
    }

    const items = bulletLines(section.body);
    if (items.length === 0) {
      errors.push(`Section "${section.title}" has no checklist items.`);
      continue;
    }

    for (const item of items) {
      if (!item.endsWith("?")) {
        errors.push(`Checklist item must end with a question mark in "${section.title}": ${item}`);
      }
    }
  }

  const sources = findSection(sections, "6. Sources");
  if (!sources) {
    errors.push("Missing sources section.");
  } else {
    const items = bulletLines(sources.body);
    if (items.length < 4) {
      errors.push("Sources section must contain at least four source entries.");
    }

    for (const item of items) {
      if (!item.includes("informed")) {
        errors.push(`Source entry must explain its contribution: ${item}`);
      }
    }
  }

  const fullText = markdown.toLowerCase();
  for (const term of ["timeout", "retry", "idempotency", "structured logs", "authorization"]) {
    if (!fullText.includes(term)) {
      errors.push(`Checklist must cover the term "${term}".`);
    }
  }

  return errors;
}
