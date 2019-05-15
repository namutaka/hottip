#!/bin/sh
# docker-entrypoint.sh
#
set -e

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    python manage.py migrate --noinput
fi

if [ "x$DJANGO_MANAGEPY_COLLECTSTATIC" = 'xon' ]; then
    python manage.py collectstatic --noinput
fi

if [ "x$DJANGO_MANAGEPY_CREATESUPERUSER" = 'xon' ]; then
    python ./manage.py shell -c 'import createsuperuser' 
fi

exec "$@"

