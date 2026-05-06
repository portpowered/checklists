.PHONY: setup typecheck lint test

setup:
	npm ci --silent

typecheck: setup
	npm run typecheck --silent

lint: setup
	npm run lint --silent

test: typecheck lint
	npm test --silent
