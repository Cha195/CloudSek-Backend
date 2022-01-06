FROM python:3.9-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt

ADD . /app
WORKDIR /app

ENV FLASK_ENV=development

CMD flask run --host=0.0.0.0