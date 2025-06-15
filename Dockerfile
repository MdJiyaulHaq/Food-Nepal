
FROM python:3.13.4-alpine3.22
LABEL maintainer="mdjiyaulhaq.com.np"

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

EXPOSE 8000

ARG DEV=false
RUN python -m venv /.venv && \
    /.venv/bin/pip install --upgrade pip && \
    /.venv/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; then \
        /.venv/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/.venv/bin:$PATH"

USER django-user
