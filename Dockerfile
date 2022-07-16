FROM python:3.9-slim-buster
USER root

WORKDIR /opt/app
COPY . .

RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py loaddata ./graphql_sample/fixtures/test.json

ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload" ]