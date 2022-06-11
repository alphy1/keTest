# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SUPERUSER_PASSWORD=11223344
ENV DJANGO_SUPERUSER_USERNAME='admin'
ENV DJANGO_SUPERUSER_EMAIL='alphiya01@mail.ru'
WORKDIR /myapp
COPY requirements.txt /myapp/
RUN pip3 install -r requirements.txt
COPY . /myapp/

RUN python manage.py migrate
RUN python manage.py createsuperuser --noinput
RUN python manage.py loaddata myapp/fixtures/populate_database.json