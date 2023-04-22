.PHONY: build data_pipeline_run data_pipeline_run_docker dbt_run dbt_run_docker \
		format_code initialize pylint pylint_errors type_check test migrations_run \
		migrations_run_docker streamlit_run

SHELL=/bin/bash -o pipefail

GCLOUD_REGION := us-east1
GCLOUD_PROJECT_ID := bjj-dashboard-383320
GCLOUD_REPO_ID := bjj-docker-repo
DOCKER_REGISTRY = $(GCLOUD_REGION)-docker.pkg.dev/$(GCLOUD_PROJECT_ID)/$(GCLOUD_REPO_ID)

VERSION_NUMBER = $(shell poetry version -s)
IMAGE_NAME := bjj-journey
IMAGE_NAME_FULL = $(DOCKER_REGISTRY)/$(IMAGE_NAME)
IMAGE_TAG = $(IMAGE_NAME_FULL):$(VERSION_NUMBER)

build:
	@echo "Building Docker image $(IMAGE_TAG)."
	@docker build --tag $(IMAGE_TAG) .

data_pipeline_run:
	@echo "Running data pipeline locally"
	@scripts/validate_tier.sh "poetry run python -m bjj_journey.data_pipeline -v"

data_pipeline_run_docker:
	@if [[ -z "$${TIER}" ]]; then \
		echo "TIER environment variable must be provided."; \
		echo "Valid tiers include dev and prod."; \
		exit 1; \
	fi
	@echo "Running data pipeline locally via docker with tier $${TIER}"
	@docker/run_locally.sh "$${TIER}" data-pipeline

dbt_run:
	@if [[ -z "$${TIER}" ]]; then \
		echo "TIER environment variable must be provided for dbt runs."; \
		echo "Valid tiers include dev and prod."; \
		exit 1; \
	fi
	@echo "Running dbt locally with target $${TIER}"
	@poetry run dbt run --project-dir dbt --target "$${TIER}" --profiles-dir ~/.dbt

dbt_run_docker:
	@if [[ -z "$${TIER}" ]]; then \
		echo "TIER environment variable must be provided."; \
		echo "Valid tiers include dev and prod."; \
		exit 1; \
	fi
	@echo "Running dbt locally via docker with tier $${TIER}"
	@docker/run_locally.sh "$${TIER}" dbt

format_code:
	@echo "Formatting code via black"
	@poetry run black streamlit_app.py src --preview

initialize:
	@echo "Initializing project via poetry"
	@poetry install

migrations_run:
	@echo Running database migrations locally via Alembic
	@scripts/validate_tier.sh "poetry run alembic upgrade head"

migrations_run_docker:
	@if [[ -z "$${TIER}" ]]; then \
		echo "TIER environment variable must be provided."; \
		echo "Valid tiers include dev and prod."; \
		exit 1; \
	fi
	@echo "Running database migrations locally via docker with tier $${TIER}"
	@docker/run_locally.sh "$${TIER}" migrations

pylint:
	@echo "Running pylint"
	@poetry run pylint streamlit_app.py src

pylint_errors:
	@echo "Running pylint --errors-only"
	@poetry run pylint streamlit_app.py src --errors-only

streamlit_run:
	@echo Running Streamlit app
	@scripts/validate_tier.sh "poetry run streamlit run streamlit_app.py"

type_check:
	@echo "Running type check via mypy"
	@poetry run mypy streamlit_app.py src

test: type_check pylint_errors
