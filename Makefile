.PHONY: format_code initialize pylint pylint_errors type_check test

format_code:
	@echo "Formatting code via black"
	@poetry run black src --preview

initialize:
	@echo "Initializing project via poetry"
	@poetry install

pylint:
	@echo "Running pylint"
	@poetry run pylint src

pylint_errors:
	@echo "Running pylint --errors-only"
	@poetry run pylint --errors-only src

type_check:
	@echo "Running type check via mypy"
	@poetry run mypy src

test: type_check pylint_errors
