"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import json
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_DIR = BASE_DIR / '.secrets'

COMMON_SECRET_FILE = SECRET_DIR / 'common.json'
COMMON_SECRET = json.loads(COMMON_SECRET_FILE.read_text())

LOCAL_SECRET_FILE = SECRET_DIR / 'local.json'
LOCAL_SECRET = json.loads(LOCAL_SECRET_FILE.read_text())

PRODUCT_SECRET_FILE = SECRET_DIR / 'product.json'
PRODUCT_SECRET = json.loads(PRODUCT_SECRET_FILE.read_text())


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4v14002&n=ew%dm%(hc@$@@d9!b8pg3%v-@csm-kr14)a5*flw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_celery_beat',
    'django_celery_results',
    'django_crontab',
    'rest_framework',
    'rules.apps.AutodiscoverRulesConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'private_storage',
    'tinymce',
    'django_filters',
    'pure_pagination',
    'django_ratelimit',
    'categories',
    'categories.editor',
    
    'core',
    'users',
    'problems',
    'submissions',
    'judge',
    'ranks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.RateLimitExceptionMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.version_hash',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = 'staticfiles'

PRIVATE_STORAGE_AUTH_FUNCTION = 'private_storage.permissions.allow_staff'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

TINYMCE_DEFAULT_CONFIG = {
    # "theme": "silver",
    "skin": "oxide-dark",
    "content_css": "dark",
    "height": 500,
    "menubar": False,
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,hr,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
    "code,help,wordcount,codesample,preview",
    "toolbar": "undo redo | formatselect | hr |"
    "bold italic backcolor | alignleft aligncenter "
    "alignright alignjustify | bullist numlist outdent indent | "
    "removeformat | fontselect | code | codesample | preview | help",
}

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 8,
    'MARGIN_PAGES_DISPLAYED': 2,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

LOGS_DIR = BASE_DIR / 'logs/'


RANK_UPDATE_CYCLE_MINUTE = 10
CRONJOBS = [
    (
        '*/%d * * * *' % RANK_UPDATE_CYCLE_MINUTE,
        'ranks.cron.update_rank',
        '>> %s' % str(LOGS_DIR / 'cron.log 2>&1'),
    ),
]

TEMP_DIR = BASE_DIR / 'temp'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}

VERSION_HASH = os.popen('git rev-parse --short HEAD').read().strip()

CSRF_TRUSTED_ORIGINS = ['https://djoj.net', 'https://www.djoj.net']
