PYTHON ?= python
VALIDATOR = scripts/validate_checklist.py

.PHONY: lint typecheck test check

lint:
	$(PYTHON) $(VALIDATOR) lint

typecheck:
	$(PYTHON) $(VALIDATOR) typecheck

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"
	$(PYTHON) $(VALIDATOR) test

check: lint typecheck test
