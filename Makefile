PYTHON ?= python
VALIDATOR = scripts/validate_checklist.py

.PHONY: setup website-lint website-typecheck website-test backend-lint backend-typecheck backend-test lint typecheck test check

setup:
	npm ci --silent

website-lint:
	$(PYTHON) $(VALIDATOR) lint

website-typecheck:
	$(PYTHON) $(VALIDATOR) typecheck

website-test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"
	$(PYTHON) $(VALIDATOR) test

backend-lint: setup
	npm run lint --silent

backend-typecheck: setup
	npm run typecheck --silent

backend-test:
	npm test --silent

lint: website-lint backend-lint

typecheck: website-typecheck backend-typecheck

test: lint typecheck website-test backend-test

check: test
