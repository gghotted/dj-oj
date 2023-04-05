from .base import *

DEBUG = PRODUCT_SECRET['DEBUG']

ALLOWED_HOSTS = PRODUCT_SECRET['ALLOWED_HOSTS']

WSGI_APPLICATION = 'milylog.wsgi.product.application'

DATABASES = {'default': PRODUCT_SECRET['DATABASES']}

CRONTAB_DJANGO_SETTINGS_MODULE = 'milylog.settings.product'
