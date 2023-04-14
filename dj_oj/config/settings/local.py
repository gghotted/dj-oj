from .base import *

DEBUG = LOCAL_SECRET['DEBUG']

ALLOWED_HOSTS = LOCAL_SECRET['ALLOWED_HOSTS']

WSGI_APPLICATION = 'config.wsgi.local.application'

if LOCAL_SECRET.get('DATABASES'):
    DATABASES = {'default': LOCAL_SECRET['DATABASES']}

CRONTAB_DJANGO_SETTINGS_MODULE = 'config.settings.local'

CELERY_BROKER_URL = 'redis://%s:6379/0' % LOCAL_SECRET['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = 'redis://%s:6379/0' % LOCAL_SECRET['CELERY_RESULT_BACKEND']

CACHES['cache-for-ratelimiting'] = {
    'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION': 'redis://%s:6379/0' % LOCAL_SECRET['CELERY_BROKER_URL'],
}
RATELIMIT_USE_CACHE = 'cache-for-ratelimiting'
RATELIMIT_ENABLE = False

VERSION_HASH = os.popen('git rev-parse --short HEAD').read().strip()
