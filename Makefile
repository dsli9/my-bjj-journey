.PHONY: dbt_run format_code initialize pylint pylint_errors type_check test \
		run_migrations run_streamlit

dbt_run:
	@echo "Running dbt"
	@poetry run dbt run --project-dir dbt

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

run_migrations:
	@echo Running database migrations via Alembic
	@poetry run alembic upgrade head

run_streamlit:
	@echo Running Streamlit app
	@poetry run streamlit run streamlit_app.py

type_check:
	@echo "Running type check via mypy"
	@poetry run mypy streamlit_app.py src

test: type_check pylint_errors
