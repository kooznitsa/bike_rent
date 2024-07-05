from datetime import timedelta
import os
from pathlib import Path

import environ

env = environ.Env()
PROJECT_NAME = env.str('PROJECT_NAME')
ENV = env.str('ENV')
VERSION = env.str('VERSION')

CORE_DIR = Path(__file__).resolve().parent
BASE_DIR = CORE_DIR.parent

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.str('DEBUG')

ALLOWED_HOSTS = env.list('URLS')

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

EXTERNAL_APPS = (
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'django_celery_beat',
    'django_celery_results',
    'drf_registration',
)

CUSTOM_APPS = (
    'bike',
    'common',
    'rent',
    'user',
)

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + CUSTOM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': ['notification/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': '.'.join((os.path.basename(CORE_DIR), 'jinja', 'environment'))
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'common/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    }
]

WSGI_APPLICATION = 'core.wsgi.application'

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),
        'PORT': env.str('POSTGRES_PORT'),
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = env.str('TZ')
USE_I18N = True
USE_TZ = True

# Static urls
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'user.User'
USER_SERIALIZER = 'user.v1.serializers.UserSerializer'

AUTHENTICATION_BACKENDS = [
    'drf_registration.auth.MultiFieldsModelBackend',
]

# DRF configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',

    # For swagger
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # Versioning
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning'
}

# Swagger
SPECTACULAR_SETTINGS = {
    'TITLE': f'{PROJECT_NAME} API',
    'DESCRIPTION': f'Endpoints for "{PROJECT_NAME}" API',
    'VERSION': 'v1',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {
        'name': 'kooznitsa',
        'url': 't.me/kooznitsa',
    },
    'LICENSE': {'name': 'BSD License'},
    'SERVE_PUBLIC': True,
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    'SCHEMA_PATH_PREFIX': r'^v\d+',
    'SCHEMA_PATH_PREFIX_TRIM': True,
    'CAMELIZE_NAMES': True,
    'ENUM_NAME_OVERRIDES': {
        'AdditionType': 'car.models.Addition.TYPE_CHOICES',
        'FuelType': 'collector.models.CollectorNotice.FUEL_CHOICES',
        'RentType': 'rent.models.Rent.TYPE_CHOICES'
    },
    'PREPROCESSING_HOOKS': ["core.excluded_paths.custom_preprocessing_hook"],
}

# Redis configuration
REDIS_LOGIN = env.str('REDIS_LOGIN')
REDIS_PASSWORD = env.str('REDIS_PASSWORD')
REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.str('REDIS_PORT')
REDIS_URL = f'redis://{REDIS_LOGIN}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'

# Celery configuration
CELERY_TIMEZONE = TIME_ZONE
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_BROKER_URL = CELERY_RESULT_BACKEND = REDIS_URL
CELERY_BROKER_HEARTBEAT = 0

# Corsheaders configuration
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = tuple('http{}://{}'.format('' if ENV == 'local' else 's', x) for x in ALLOWED_HOSTS)
BACK_URL = CSRF_TRUSTED_ORIGINS[0]

# JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=4),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'uid',
    'USER_ID_CLAIM': 'user_uid',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}
