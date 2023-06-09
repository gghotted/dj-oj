from .base import *

DEBUG = PRODUCT_SECRET['DEBUG']

ALLOWED_HOSTS = PRODUCT_SECRET['ALLOWED_HOSTS']

WSGI_APPLICATION = 'config.wsgi.product.application'

DATABASES = {'default': PRODUCT_SECRET['DATABASES']}

CRONTAB_DJANGO_SETTINGS_MODULE = 'config.settings.product'

CELERY_BROKER_URL = 'redis://%s:6379/0' % PRODUCT_SECRET['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = 'redis://%s:6379/0' % PRODUCT_SECRET['CELERY_RESULT_BACKEND']

BASE_DIR_FROM_HOST = PRODUCT_SECRET['BASE_DIR_FROM_HOST']

CACHES['cache-for-ratelimiting'] = {
    'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION': 'redis://%s:6379/0' % PRODUCT_SECRET['CELERY_BROKER_URL'],
}
RATELIMIT_USE_CACHE = 'cache-for-ratelimiting'

VERSION_HASH = os.environ.get('VERSION_HASH')
