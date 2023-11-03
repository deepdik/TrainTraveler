# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

ENV ENV=DEV
RUN apt-get install -y libgdal-dev
RUN apt-get install -y cron
RUN apt-get install -y vim nano

# RUN apt-get install memcached
# RUN systemctl start memcached


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]