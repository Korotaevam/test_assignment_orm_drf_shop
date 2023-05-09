#!/bin/bash

python manage.py collectstatic
python manage.py migrate
python manage.py loaddata ./fixtures/city.json
python manage.py loaddata ./fixtures/street.json
python manage.py loaddata ./fixtures/shop.json

exec "$@"