.PHONY: dbt_run format_code initialize pylint pylint_errors type_check test \
		run_migrations run_streamlit

SHELL=/bin/bash -o pipefail

dbt_run:
	@if [[ -z "$${TIER}" ]]; \
		then \
		echo "TIER environment variable must be provided for dbt runs."; \
		echo "Valid tiers include dev and prod."; \
		exit 1; \
	fi
	@echo "Running dbt with target $${TIER}"
	@poetry run dbt run --project-dir dbt --target "$${TIER}"

format_code:
	@echo "Formatting code via black"
	@poetry run black streamlit_app.py src --preview

initialize:
	@echo "Initializing project via poetry"
	@poetry install

pylint:
	@echo "Running pylint"
	@poetry run pylint streamlit_app.py src

pylint_errors:
	@echo "Running pylint --errors-only"
	@poetry run pylint streamlit_app.py src --errors-only

migrations_run:
	@echo Running database migrations via Alembic
	@scripts/validate_tier.sh "poetry run alembic upgrade head"

data_pipeline_run:
	@echo Running data pipeline
	@scripts/validate_tier.sh "poetry run python -m bjj_journey.data_pipeline -v"

streamlit_run:
	@echo Running Streamlit app
	@scripts/validate_tier.sh "poetry run streamlit run streamlit_app.py"

type_check:
	@echo "Running type check via mypy"
	@poetry run mypy streamlit_app.py src

test: type_check pylint_errors
