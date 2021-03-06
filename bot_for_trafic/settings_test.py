"""
Django settings for bot_for_trafic project.

Generated by 'django-admin startproject' using Django 1.11.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

from django.urls import reverse_lazy

from .disable_migrations_in_test import DisableMigrations
from .base_conf import BaseConf

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-dl@6shqqobkyp8z%*p!sal&apnfu3-2ibk#y#8e1cf)3ni#c-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = BaseConf.DEBUG_MAIN

ALLOWED_HOSTS = BaseConf.MAIN_SITE_URL


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_for_trafic.apps.AppForTraficConfig',
    'rest_framework',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'bot_for_trafic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bot_for_trafic.wsgi.application'

# RUN TEST CONFIG
MIGRATION_MODULES = DisableMigrations()
TEST_RUNNER = 'app_for_trafic.custom_test_runner.UnManagedModelTestRunner'
FIXTURE_DIRS = os.path.join(BASE_DIR, 'app_for_trafic', 'fixtures')
FIXTURE_FILES = os.path.join(FIXTURE_DIRS, 'fixture_for_testing.json')
TEST_SETTINGS_CONFIG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = BaseConf.DATABASES_MAIN_SQLITE
CELERY_BROKER_URL = BaseConf.CELERY_BROKER_URL
CELERY_RESULT_BACKEND = BaseConf.CELERY_RESULT_BACKEND
# CELERY_BROKER_TRANSPORT_OPTIONS = BaseConf.CELERY_BROKER_TRANSPORT_OPTIONS
CELERY_ACCEPT_CONTENT = BaseConf.CELERY_ACCEPT_CONTENT
CELERY_TASK_SERIALIZER = BaseConf.CELERY_TASK_SERIALIZER
CELERY_RESULT_SERIALIZER = BaseConf.CELERY_RESULT_SERIALIZER
CELERY_TIMEZONE = BaseConf.CELERY_TIMEZONE
CELERY_ENABLE_UTC = BaseConf.CELERY_ENABLE_UTC
CELERY_BEAT_SCHEDULE = BaseConf.CELERY_BEAT_SCHEDULE
CELERY_TASK_RESULT_EXPIRES = BaseConf.CELERY_TASK_RESULT_EXPIRES
CELERY_IMPORTS = BaseConf.CELERY_IMPORTS

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': ('app_for_trafic.utils.auth.CustomTokenAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_REQUIREMENTS': None,
    'SECURITY_DEFINITIONS': {
        "api_key": {
            "type": "apiKey",
            "name": "X-Auth-Token",
            "in": "header"
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, 'app_for_trafic', 'locale'),)

LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')

TIME = 3 * 60 * 60
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = TIME
SESSION_IDLE_TIMEOUT = TIME

LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app_for_trafic.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': 1024*1024*10,
            'backupCount': 5,
            'formatter': 'verbose'
        },
        'telegram': {
            'level': 'WARNING',
            'class': 'app_for_trafic.custom_loggers.TelegramLogHandler',
            'formatter': 'verbose'
        },
        'celery': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': 1024 * 1024 * 20,
            'backupCount': 5,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null', 'telegram'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.db': {
            'handlers': ['console', 'file', 'telegram'],
            'propagate': True,
            'level': 'INFO',
        },
        'celery': {
            'handlers': ['celery', 'console', 'telegram'],
            'level': 'INFO',
        },
        'celery.task': {
            'handlers': ['celery', 'console', 'telegram'],
            'level': 'INFO',
        },
        'app_for_trafic.utils.mail': {
            'handlers': ['console', 'file', 'telegram'],
            'level': 'INFO',
        },
        'app_for_trafic.utils.templateletter': {
            'handlers': ['console', 'file', 'telegram'],
            'level': 'INFO',
        }
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

PORTAL_URL = 'https://{}'.format(BaseConf.SITE_URL_BASE)

STATIC_ROOT = '../static/'

MEDIA_ROOT = '../media/'

