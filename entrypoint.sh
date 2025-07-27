#!/bin/sh
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

python manage.py migrate --no-input
python manage.py collectstatic --no-input

exec "$@"