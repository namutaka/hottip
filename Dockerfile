#
# Dockerfile
#

#
# stage: build frontend 
#
FROM node:11.12 as frontend_builder

WORKDIR /build/

RUN npm install -g yarn

COPY /frontend/ ./

RUN set -x \
  && yarn install \
  && yarn build


#
# stage: build service image
#
FROM python:3.7.2
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN set -ex \
  && pip install pipenv \
  && pipenv install --system --deploy

COPY --from=frontend_builder \
  /build/dist/static ./hottip/
COPY --from=frontend_builder \
  /build/dist/index.html ./hottip/templates/hottip/
COPY . .

EXPOSE 8080

ENV DJANGO_SETTINGS_MODULE=hottip_proj.settings

# uWSGI configuration (customize as needed):
ENV \
  UWSGI_WSGI_FILE=hottip_proj/wsgi.py \
  UWSGI_HTTP=:8080 \
  UWSGI_MASTER=1 \
  UWSGI_WORKERS=1 \
  UWSGI_THREADS=8 \
  UWSGI_UID=1000 \
  UWSGI_GID=2000 \
  UWSGI_LAZY_APPS=1 \
  UWSGI_WSGI_ENV_BEHAVIOR=holy \
  UWSGI_STATIC_MAP="/static/=/app/static/"  \
  UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN DATABASE_TYPE=none \
    python manage.py collectstatic --noinput

# Start uWSGI
CMD ["uwsgi", "--http-auto-chunked", "--http-keepalive"]

