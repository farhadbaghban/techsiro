FROM python:3.12.6-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src
COPY  techsiro/requirments src/requirements

RUN apt-get update  && \
    apt-get install -y libpq-dev && \
    pip install --upgrade pip && \
    pip install -r src/requirements/dev.requirements.txt

EXPOSE 8000

COPY . /src
RUN chmod +x ./docker_entrypoint.sh
ENTRYPOINT "./docker_entrypoint.sh"



