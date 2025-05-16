#Building stage
FROM python:3.10-slim AS builder

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

#Final environment
FROM python:3.10-slim AS web-server

RUN useradd -m django-user

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /home/django-user/app

COPY --chown=django-user:django-user . .

USER django-user

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

