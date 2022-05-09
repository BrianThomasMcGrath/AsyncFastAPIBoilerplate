FROM python:slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install and setup poetry
RUN pip install -U pip \
    && apt-get update \
    && apt install -y curl netcat \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /usr/app
COPY . .
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY source source
COPY scripts scripts

WORKDIR /usr/app/source

EXPOSE 5000

CMD ["uvicorn","app.main:app", "--port", "5000"]