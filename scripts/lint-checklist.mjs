// @ts-check

import { readChecklist, validateChecklist } from "./checklist-rules.mjs";

const checklist = readChecklist();
const errors = validateChecklist(checklist);

if (errors.length > 0) {
  for (const error of errors) {
    console.error(`- ${error}`);
  }

  process.exitCode = 1;
} else {
  console.log("Checklist lint passed.");
}
