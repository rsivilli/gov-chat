FROM python:3.10.12-bookworm

EXPOSE 8000

ENV POETRY_VERSION=1.4.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1




# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}



# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"


WORKDIR /app

COPY ../../. /app
RUN poetry install


# This is required for chatserver and webcrawler
RUN poetry run pip install torch --extra-index-url https://download.pytorch.org/whl/cu113

#This is required for webscrape
RUN apt-get update 
RUN apt-get install -y chromium chromium-driver


# Install dependencies

# waiter entry point
COPY ../../docker_entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]


# Run your app

CMD [ "poetry", "run", "python", "-c", "print('Hello, World!')" ]
