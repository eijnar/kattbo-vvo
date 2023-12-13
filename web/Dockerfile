FROM python:3.12.1-slim as base

WORKDIR /usr/src/kattbo-vvo

COPY ./web /usr/src/kattbo-vvo
COPY ./common /tmp/common

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install /tmp/common

RUN addgroup --system appuser && adduser --system --group appuser
RUN chown -R appuser:appuser /usr/src/kattbo-vvo
USER appuser

FROM base as web
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]

FROM base as web_celery_worker
CMD ["celery", "-A", "app.celery", "worker", "-E", "--loglevel=info"]
