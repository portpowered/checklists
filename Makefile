PYTHON ?= python
VALIDATOR = scripts/validate_checklist.py

.PHONY: website-lint website-typecheck website-test lint typecheck test check

website-lint:
	$(PYTHON) $(VALIDATOR) lint

website-typecheck:
	$(PYTHON) $(VALIDATOR) typecheck

website-test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"
	$(PYTHON) $(VALIDATOR) test

lint: website-lint

typecheck: website-typecheck

test: lint typecheck website-test

check: test
