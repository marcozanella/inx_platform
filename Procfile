web: PYTHONUNBUFFERED=1 python manage.py runserver 0.0.0.0:21013
worker: watchmedo auto-restart --patterns="*.py" --recursive -- celery -A django_inx_platform worker -n localhost --loglevel=info -E
beat: PYTHONUNBUFFERED=1 celery -A django_inx_platform beat --loglevel=info
flower: PYTHONUNBUFFERED=1 celery -A django_inx_platform flower