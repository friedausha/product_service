"""
Django settings for product_service project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import pymysql

from product_service.middleware.profiling_middleware import ProfilingMiddleware

pymysql.install_as_MySQLdb()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import environ
env = environ.Env(DEBUG=(bool, False))

environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a9*dfqbho-*pzdzfh6v$f5d(*#6=kxk7gm9%2v5&#xqq3tw-2u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ALLOWED_HOSTS = ['localhost']

# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Add your custom middleware here
    'product_service.middleware.token_auth_middleware.TokenAuthMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # 'product_service.middleware.profiling_middleware.ProfilingMiddleware',
)
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.profiling.ProfilingPanel',  # Add profiling panel
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.sql.SQLPanel',
]
INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,  # Show only when DEBUG is True
}

ROOT_URLCONF = 'product_service.urls'

WSGI_APPLICATION = 'product_service.wsgi.application'

CSRF_TRUSTED_ORIGINS = ['127.0.0.1', 'localhost']

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME', default='product_entrytask_db'),
        'USER': env('DB_USER', default='your_name'),
        'PASSWORD': env('DB_PASSWORD', default='your_password'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='3308'),
    }
}
# USER_SERVICE = "http://host.docker.internal:8080/"
# USER_SERVICE = "localhost:8080"
USER_SERVICE = ('localhost', 8080)
# USER_SERVICE = ('host.docker.internal', 8080)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PORT = 8001
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logfile.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
    'product_service.middleware.profiling_middleware': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }