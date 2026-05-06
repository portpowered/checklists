PYTHON ?= python
VALIDATOR = scripts/validate_checklist.py

.PHONY: lint typecheck test check

lint:
	$(PYTHON) $(VALIDATOR) lint

typecheck:
	$(PYTHON) $(VALIDATOR) typecheck

test:
	$(PYTHON) $(VALIDATOR) test

check: lint typecheck test
