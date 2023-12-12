FROM python:3.12.1-slim

WORKDIR /usr/src/kattbo-vvo

COPY . /usr/src/kattbo-vvo

RUN pip install --no-cache-dir -r requirements.txt
RUN addgroup --system appuser && adduser --system --group appuser
RUN chown -R appuser:appuser /usr/src/kattbo-vvo

USER appuser

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]