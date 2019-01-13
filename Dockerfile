FROM python:3.7.0-alpine3.8

MAINTAINER Nick Groesz <nick.groesz@gmail.com>

COPY ./requirements.txt /var/app/current/web_service/requirements.txt

WORKDIR /var/app/current/web_service

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev

RUN pip3 install -r requirements.txt --no-deps

COPY . /var/app/current/web_service

EXPOSE 5000

ENV FLASK_ENV development
ENV FLASK_APP flasky.py

ENTRYPOINT [ "flask", "runserver" ]
