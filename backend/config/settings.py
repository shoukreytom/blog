from pathlib import Path
import os
from datetime import timedelta
import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

if os.path.exists(os.path.join(BASE_DIR/'config', 'hidden.py')):
    from .hidden import *
else:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG      = os.environ.get('DEBUG_VALUE')

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # local apps
    'blog',
    'users',
    'api',

    # 3rd party apps
    'rest_framework',
    'rest_framework_jwt',
    'corsheaders',
    # 'tailwind',
    # 'frontend',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',    #3rd party
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# TAILWIND_APP_NAME = 'frontend'
AUTH_USER_MODEL = 'users.User'
ROOT_URLCONF = 'config.urls'
CORS_ALLOW_ALL_ORIGINS = True   # TODO: comment this line after test
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:443",
]

REST_FRAMEWORK = {
     'DEFAULT_PERMISSION_CLASSES': [
         'rest_framework.permissions.IsAuthenticated',
         ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
     'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
     )
}

JWT_AUTH = {
  'JWT_ENCODE_HANDLER':
  'rest_framework_jwt.utils.jwt_encode_handler',
  'JWT_DECODE_HANDLER':
  'rest_framework_jwt.utils.jwt_decode_handler',
  'JWT_PAYLOAD_HANDLER':
  'rest_framework_jwt.utils.jwt_payload_handler',
  'JWT_PAYLOAD_GET_USER_ID_HANDLER':
  'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
  'JWT_RESPONSE_PAYLOAD_HANDLER':
  'rest_framework_jwt.utils.jwt_response_payload_handler',
 
  'JWT_SECRET_KEY': 'SECRET_KEY',
  'JWT_GET_USER_SECRET_KEY': None,
  'JWT_PUBLIC_KEY': None,
  'JWT_PRIVATE_KEY': None,
  'JWT_ALGORITHM': 'HS256',
  'JWT_VERIFY': True,
  'JWT_VERIFY_EXPIRATION': True,
  'JWT_LEEWAY': 0,
  'JWT_EXPIRATION_DELTA': timedelta(days=30),
  'JWT_AUDIENCE': None,
  'JWT_ISSUER': None,
  'JWT_ALLOW_REFRESH': False,
  'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30),
  'JWT_AUTH_HEADER_PREFIX': 'Bearer',
  'JWT_AUTH_COOKIE': None,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

django_heroku.settings(locals())
X_FRAME_OPTIONS = 'SAMEORIGIN'
