import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = 'django-insecure-(-7_0j7bhdb$dd#&gm*qv^06i!3$8rtw9p4^bdkrpi^p$hav6e'
# DEBUG = True

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# False if not in os.environ
DEBUG = env('DEBUG')

# SECRET_KEY = env('SECRET_KEY')
SECRET_KEY = '-7_0j7bhdb$dd#&gm*qv^06i!3$8rtw9p4^bdkrpi^p$hav6e'

# DATABASES = {
#     # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
#     'default': env.db('DATABASE_URL'),
# }
import dj_database_url

DATABASES = {'default': dj_database_url.config()}

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    # 'api.apps.AppConfig',
    'api',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
    'django_filters',
    'corsheaders',
    'django_jalali',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',  # برای دسترسی به کاربر جاری در مدل
]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
]
ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
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

WSGI_APPLICATION = 'backend.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db2.sqlite3',
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
# LANGUAGE_CODE = 'fa-ir'
import locale

# locale.setlocale(locale.LC_ALL, "fa_IR.UTF-8")
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True
USE_THOUSAND_SEPARATOR = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GRAPHENE = {
    "SCHEMA": "backend.schema.schema",
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]
# authorization
# {"authorization":"jwt token"}
AUTH_USER_MODEL = 'api.User'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/api/'
LOGOUT_URL = 'logout'

HAVE_NOT_PERMISSION = 'you have not permission !!'

IMPORT_EXPORT_SKIP_ADMIN_LOG = True
