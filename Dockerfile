FROM --platform=linux/x86_64 python:3.8-slim as python-base

# Configure Poetry
# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.3.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Create stage for Poetry installation
FROM python-base as poetry-base

# Create a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Create a new stage from the base python image
FROM python-base as bjj-journey

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Set working directory
WORKDIR /usr/share/my-bjj-journey

# Copy poetry files and install dependencies
COPY poetry.lock pyproject.toml README.md ./
COPY src/ ./src/
RUN poetry install -v --no-interaction --no-cache --only docker

# Copy necessary files and folders
COPY profiles.yml ./
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY dbt/ ./dbt/

# Copy entrypoint script that will be run upon build completion
COPY ./docker/entrypoint.sh /usr/share/entrypoint/entrypoint.sh

# Run entrypoint script
ENTRYPOINT ["/usr/share/entrypoint/entrypoint.sh"]
CMD ["/usr/share/my-bjj-journey/"]
