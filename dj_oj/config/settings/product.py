from .base import *

DEBUG = PRODUCT_SECRET['DEBUG']

ALLOWED_HOSTS = PRODUCT_SECRET['ALLOWED_HOSTS']

WSGI_APPLICATION = 'milylog.wsgi.product.application'

DATABASES = {'default': PRODUCT_SECRET['DATABASES']}

CRONTAB_DJANGO_SETTINGS_MODULE = 'milylog.settings.product'

CELERY_BROKER_URL = 'redis://%s:6379/0' % PRODUCT_SECRET['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = 'redis://%s:6379/0' % PRODUCT_SECRET['CELERY_RESULT_BACKEND']
