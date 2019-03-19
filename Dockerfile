#
# Dockerfile
#

FROM python:3.7.2

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
COPY . .

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

