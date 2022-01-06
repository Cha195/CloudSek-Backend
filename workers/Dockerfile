FROM python:3.9-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt

ADD . /workers
WORKDIR /workers

ENTRYPOINT celery -A task worker --loglevel=INFO --pool=solo
