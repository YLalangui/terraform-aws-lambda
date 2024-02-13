FROM python:3.10

RUN apt-get update --fix-missing
RUN apt-get install -y git make

ENV PYTHONDONTWRITEBYTECODE 1

ENV HOMEDIR=/app
RUN mkdir -p $HOMEDIR
COPY . $HOMEDIR
WORKDIR $HOMEDIR
ENV PYTHONPATH='$PYTHONPATH:/app'

# Persist bash command history
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && echo "$SNIPPET" >> "/root/.bashrc"

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --only main --no-root