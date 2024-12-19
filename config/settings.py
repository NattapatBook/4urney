"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

import pydash
from environ import environ

from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENV = environ.Env()  # use uppercase allow using via django.conf.settings
ENV.read_env(env_file=str(BASE_DIR / '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV('SECRET_KEY', str, default='django-insecure-fm)$u4d@+v75_8fzihaty!y*+*dv_og18^@j0wpkp!*5v&u&gs')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV('DEBUG', bool, default=True)

HOST_NAME = ENV('HOST_NAME', str, default='')
ALLOWED_HOSTS = ['localhost', 'backend'] + ([HOST_NAME] if HOST_NAME else [])
CSRF_TRUSTED_ORIGINS = ['http://localhost:8080'] + ([f'https://{HOST_NAME}'] if HOST_NAME else [])
CORS_ALLOWED_ORIGINS = ["http://localhost:8000",'https://webhook.site']
CORS_ALLOW_HEADERS = (    *default_headers,    "x-line-signature",)

# Application definition
ALLOWED_APPS = ENV('ALLOWED_APPS', list, default=[])

PROJECT_APPS = [
    app_name
    for app_name in os.listdir('apps')
    if os.path.exists(f'apps/{app_name}/apps.py')
    if not ALLOWED_APPS or app_name in ALLOWED_APPS
]
print(os.listdir('apps'))

INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'control.apps.ControlConfig',
    *[
        f'apps.{app_name}.apps.{pydash.pascal_case(app_name)}Config'
        for app_name in PROJECT_APPS
    ],
    'migrator.apps.MigratorConfig',  # help handle post_final_migrate signal
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MIDDLEWARE = [
    'config.healthcheck.HealthCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
            ],
        },
    },
]

ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if ENV('DB_HOST', str, ''):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': ENV('DB_NAME', str, 'postgres'),
            'USER': ENV('DB_USER', str, 'postgres'),
            'HOST': ENV('DB_HOST', str, 'db'),
            'PORT': ENV('DB_PORT', int, 5432),
            'PASSWORD': ENV('DB_PASS', str, ''),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'static/'
STATICFILES_DIRS = [
    "./vue/dist/",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
REDIS_ADDRESS = ENV('REDIS_ADDRESS', str, 'redis://redis:6379')  # use rediss:// for elasticache
CHANNEL_LAYERS = {
   "default": {
       # "BACKEND": "channels_redis.core.RedisChannelLayer",
       "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
       "CONFIG": {
           "hosts": ({
               "address": f'{REDIS_ADDRESS}/0',
           },),
       },
   },
}
CACHES = {
   "default": {
       "BACKEND": "django_redis.cache.RedisCache",
       "LOCATION": f'{REDIS_ADDRESS}/1',
       "OPTIONS": {
           "CLIENT_CLASS": "django_redis.client.DefaultClient"
       },
   }
}

CELERY_BROKER_URL = f'{REDIS_ADDRESS}/2'
CELERY_TIME_ZONE = TIME_ZONE
CELERY_WORKER_REDIRECT_STDOUTS_LEVEL = 'DEBUG'

# visit: rest_framework/settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'control.rest_framework.authentication.LongTokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'control.rest_framework.permissions.FullDjangoModelPermissions',
    ],
}

LOGIN_URL = '/api/control/login/'
