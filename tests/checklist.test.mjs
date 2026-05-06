// @ts-check

import test from "node:test";
import assert from "node:assert/strict";

import {
  CHECKLIST_FILE,
  REQUIRED_HEADINGS,
  extractSections,
  readChecklist,
  validateChecklist
} from "../scripts/checklist-rules.mjs";

test("the repository ships the backend checklist artifact", () => {
  const checklist = readChecklist();
  assert.ok(checklist.includes("# Backend Development Checklist"), `${CHECKLIST_FILE} should start with the backend checklist title.`);
});

test("the checklist satisfies the repository lint rules", () => {
  const checklist = readChecklist();
  assert.deepEqual(validateChecklist(checklist), []);
});

test("every required heading appears exactly once", () => {
  const sections = extractSections(readChecklist());

  for (const heading of REQUIRED_HEADINGS) {
    const matches = sections.filter((section) => section.title === heading);
    assert.equal(matches.length, 1, `Expected exactly one "${heading}" heading.`);
  }
});

test("all reviewer-facing checklist sections contain multiple observable checks", () => {
  const sections = extractSections(readChecklist())
    .filter((section) => /^[1-5](\.\d+)? /.test(section.title));

  for (const section of sections) {
    const items = section.body
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => line.startsWith("- "));

    assert.ok(items.length >= 3, `Expected at least three checklist items in "${section.title}".`);
    assert.ok(items.every((line) => line.endsWith("?")), `Expected all checklist items in "${section.title}" to be reviewer-verifiable questions.`);
  }
});
