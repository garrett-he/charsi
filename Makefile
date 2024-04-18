.DEFAULT_GOAL := help

.PHONY: help
help: ## show help information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: deps
deps: ## install dependencies and git hooks
	poetry install
	poetry run pre-commit install

.PHONY: lint
lint: ## code analyse and lint
	poetry run pylint src/ tests/

.PHONY: test
test: ## run tests in current python version
	poetry run pytest --cov=src --cov-report=term-missing

.PHONY: build
build: ## build project
	poetry build

.PYONY: build-pyi
build-pyi: ## build project with pyinstaller
	rm -rf build/ dist/
	poetry run pyinstaller charsi.spec
	cp {CHANGELOG.md,LICENSE,README.md} dist/

.PHONY: publish
publish: build ## build and publish to remote
	poetry publish

.PHONY: codecov
codecov: ## upload coverage.xml to codecov.com
	poetry run pytest --cov=src --cov-report=xml
	codecov

.PHONY: clean
clean: ## clean up cache files
	rm -rf .pytest_cache/ .tox/ build/ dist/
	rm -f .coverage coverage.xml
