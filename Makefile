.PHONY: test

# This repository currently ships checklist documents rather than executable
# application code, so the repository-native quality gate is a clean diff
# check for tracked changes.
test:
	git diff --check -- . ':(exclude)prd.json' ':(exclude)prd.md' ':(exclude)progress.txt'
