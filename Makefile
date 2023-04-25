.PHONY: build clean data_pipeline_run data_pipeline_run_docker dbt_run dbt_run_docker \
		format_code initialize pylint pylint_errors type_check test migrations_run \
		migrations_run_docker streamlit_run bump_version_patch_commit \
		bump_version_major bump_version_minor bump_version_patch bump_version_release \
		docker_push_latest docker_push_tag terraform_apply terraform_destroy

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

bump_version_major:
	@echo "Bumping major version. Current version is $(VERSION_NUMBER)"
	@poetry run python bumpversion major --verbose

bump_version_minor:
	@echo "Bumping minor version. Current version is $(VERSION_NUMBER)"
	@poetry run bumpversion minor --verbose

bump_version_patch:
	@echo "Bumping patch version. Current version is $(VERSION_NUMBER)"
	@poetry run bumpversion patch --verbose

bump_version_patch_commit:
	@echo "Bumping patch version. Current version is $(VERSION_NUMBER)"
	@poetry run bumpversion patch --verbose --commit

bump_version_release:
	@echo "Bumping version to a firm release. Current version is $(VERSION_NUMBER)"
	@poetry run bumpversion release --verbose --commit --tag

clean:
	@echo "Checking for dangling docker images."
	@to_delete="$(shell docker images -f reference=$(IMAGE_NAME_FULL) -f dangling=true -q)"
	@if [ -n "${to_delete}" ]; then\
		echo "Deleting dangling images."; \
		docker rmi -f ${to_delete}; \
	fi

data_pipeline_run:
	@echo "Running data pipeline locally"
	@scripts/validate_tier.sh
	@poetry run python -m bjj_journey.data_pipeline -v

data_pipeline_run_docker:
	@echo "Running data pipeline locally via docker"
	@scripts/validate_tier.sh
	@docker/run_locally.sh "$${TIER}" data-pipeline

dbt_run:
	@echo "Running dbt locally"
	@scripts/validate_tier.sh
	@poetry run dbt run --project-dir dbt --target "$${TIER}" --profiles-dir ~/.dbt

dbt_run_docker:
	@echo "Running dbt locally via docker"
	@scripts/validate_tier.sh
	@docker/run_locally.sh "$${TIER}" dbt

format_code:
	@echo "Formatting code via black"
	@poetry run black streamlit_app.py src scripts --preview

initialize:
	@echo "Initializing project via poetry"
	@poetry install

migrations_run:
	@echo "Running database migrations locally"
	@scripts/validate_tier.sh
	@poetry run alembic upgrade head

migrations_run_docker:
	@echo "Running database migrations locally via docker"
	@scripts/validate_tier.sh
	@docker/run_locally.sh "$${TIER}" migrations

pylint:
	@echo "Running pylint"
	@poetry run pylint streamlit_app.py src

pylint_errors:
	@echo "Running pylint --errors-only"
	@poetry run pylint streamlit_app.py src --errors-only

docker_push_tag:
	@echo "Releasing tag $(IMAGE_TAG) to remote repository."
	@docker push $(IMAGE_TAG)

docker_push_latest:
	@echo "Releasing tag $(LATEST_TAG) to remote repository."
	@docker tag $(IMAGE_TAG) $(LATEST_TAG)
	@docker push $(LATEST_TAG)

streamlit_run:
	@echo Running Streamlit app
	@scripts/validate_tier.sh "poetry run streamlit run streamlit_app.py"

terraform_apply:
	@echo Running terraform apply
	@terraform -chdir=terraform apply

terraform_destroy:
	@echo Running terraform destroy
	@terraform -chdir=terraform destroy

type_check:
	@echo "Running type check via mypy"
	@poetry run mypy streamlit_app.py src

test: type_check pylint_errors
release: clean test build docker_push_tag
