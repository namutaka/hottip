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

RUN groupadd -r -g 999 app \
  && useradd -r -g app -u 999 app

WORKDIR /app
RUN chown 999 /app

COPY Pipfile Pipfile.lock ./

RUN set -ex \
  && pip install pipenv \
  && pipenv install --system --deploy

COPY --from=frontend_builder \
  /build/dist/static ./hottip/static
COPY --from=frontend_builder \
  /build/dist/*.png ./hottip/static/
COPY --from=frontend_builder \
  /build/dist/index.html ./hottip/templates/hottip/
COPY . .

ENV DJANGO_SETTINGS_MODULE=hottip_proj.settings

# uWSGI configuration
ENV \
  UWSGI_WSGI_FILE=hottip_proj/wsgi.py \
  UWSGI_HTTP=:8080 \
  UWSGI_MASTER=1 \
  UWSGI_WORKERS=1 \
  UWSGI_THREADS=8 \
  UWSGI_UID=999 \
  UWSGI_GID=999 \
  UWSGI_LAZY_APPS=1 \
  UWSGI_WSGI_ENV_BEHAVIOR=holy \
  UWSGI_STATIC_MAP="/static/=/app/static/"  \
  UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000" \
  UWSGI_LOG_FORMAT="host:%(addr) time:%(time) method:%(method) uri:%(uri) proto:%(proto) status:%(status) size:%(size) referer:%(referer) ua:%(uagent)"

# Call collectstatic
RUN DATABASE_TYPE=none \
    python manage.py collectstatic --noinput

USER app

EXPOSE 8080

ENTRYPOINT [ "./docker-entrypoint.sh" ]

# Start uWSGI
CMD ["uwsgi", "--http-auto-chunked", "--http-keepalive"]

