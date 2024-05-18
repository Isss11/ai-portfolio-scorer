FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt gunicorn

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 src.app:app