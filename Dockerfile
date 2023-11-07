FROM python:3.12.0-alpine3.17

WORKDIR /app

RUN pip install django

COPY ./pdfdoccreator ./pdfdoccreator
COPY ./manage.py ./manage.py
EXPOSE 3000

ENTRYPOINT python3 manage.py runserver 0.0.0.0:3000