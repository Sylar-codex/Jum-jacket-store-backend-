"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from PIL import Image
import os
import dj_database_url

from corsheaders.defaults import default_headers

import redis


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG_VAL", "False") == "True"

ALLOWED_HOSTS = [os.environ.get("PRODUCTION_HOST"),os.environ.get("FRONTEND_HOST"),os.environ.get("DEVELOPMENT_HOST")]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'cloudinary',
    'cloudinary_storage',
    'commerce',
    'accounts',
    'knox',
    'wallet',
    'corsheaders',
]


REST_FRAMEWORK = {
    'DEFAULT_AUNTHENTICATION_CLASSES' :
    ('knox.auth.TokenAuthentication',),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

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

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


DATABASES['default'] = dj_database_url.config(
    conn_max_age=600,
    conn_health_checks=True,
)


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
     'http://localhost:3000',
     "https://"+os.environ.get("FRONTEND_HOST"),
     "https://"+os.environ.get("DEVELOPMENT_HOST")
]

CORS_ALLOW_ALL_ORIGINS: True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CSRF_TRUSTED_ORIGINS = [
    "https://"+os.environ.get("FRONTEND_HOST"),
    'http://localhost:3000'
]

HUEY = {
    "name": "ecommerce",
    "huey_class": "huey.PriorityRedisExpireHuey",
    "immediate": False,
    "utc": True,
    "consumer": {
        "workers": 2,
        "worker_type": "thread",
        "initial_delay": 0.1,
        "backoff": 1.15,
        "max_delay": 10.0,
        "scheduler_interval": 1,
        "periodic": True,
        "check_worker_health": True,
    },
}

from huey import RedisHuey
from redis import ConnectionPool

pool = ConnectionPool(
    host="oregon-redis.render.com",
    port=6379,
    username=os.environ.get("REDIS_USERNAME"),
    password=os.environ.get("REDIS_PASSWORD"),
    max_connections=20,
)
HUEY = RedisHuey("wallet", connection_pool=pool)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME' : os.environ.get("CLOUDINARY_CLOUD_NAME"), 
    'API_KEY' :os.environ.get("CLOUDINARY_API_KEY"),
    'API_SECRET':os.environ.get("CLOUDINARY_SECRET_KEY")
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASS")


PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")