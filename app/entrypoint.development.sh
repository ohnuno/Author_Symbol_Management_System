#!/bin/sh

if ["$DATABASE" = "postgres"
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate
python manage.py migrate django_celery_results
python manage.py collectstatic --no-input --clear
python manage.py loaddata CutterSanbornThreeFigureAuthorTable_initial_data.json
python manage.py loaddata LanguageCode_initial_data.json
python manage.py loaddata SubjectCode_initial_data.json
python manage.py loaddata Author_initial_data.json

exec "$@"
