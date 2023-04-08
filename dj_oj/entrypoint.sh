export DJANGO_SETTINGS_MODULE=config.settings.product
sleep 5 && \
python manage.py migrate && \
echo "yes" | python manage.py collectstatic && \
python manage.py crontab add && \
python manage.py crontab show && \

celery -A config worker -l debug --concurrency=2 &
gunicorn --log-level=DEBUG --bind 0.0.0.0:8000 --timeout 1200 config.wsgi.product:application