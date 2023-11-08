FROM python:3.12.0-alpine3.17

ENV PORT=3000

WORKDIR /app

RUN pip install django
RUN pip install requests
RUN pip install reportlab
RUN pip install lorem_text
RUN pip install faker
RUN pip install ebooklib

COPY ./pdfdoccreator ./pdfdoccreator
COPY ./manage.py ./manage.py
EXPOSE ${PORT}

RUN python3 manage.py migrate
ENTRYPOINT python3 manage.py runserver 0.0.0.0:${PORT}