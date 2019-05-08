
How To Setup
---------

Write `.env` file

```
HOTTIP_SLACK_WEBHOOK_URL={SLACK_INCOMING_WEBHOOK_URL}
HOTTIP_BATCH_MODE=1

DATABASE_TYPE=postgresql
DATABASE_NAME=hottip
DATABASE_USER=hottip
DATABASE_PASSWORD=password
DATABASE_HOST=localhost

# google oauth2 key & secret
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=
```

Run commands

```
$ docker-compose up -d
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py createsuperuser
Enter admin user information.
```

