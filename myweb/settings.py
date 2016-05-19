"""
Django settings for myweb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7(iy#11%mux!je_a!3c5n6vh0%e!m6qi(oc*l7e#ogz$z*y9d6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*', ]

if 'SERVER_SOFTWARE' in os.environ:
    MYSQL_DB = 'poRXGyHCZRiVajfpmWPL'
    MYSQL_USER = 'dce9b62692b7446391f52cca2840784e'
    MYSQL_PASS = '86558724fa9d48ab91a5283a2bb3d061'
    MYSQL_HOST_M = 'sqld.duapp.com'
    MYSQL_HOST_S = 'sqld.duapp.com'
    MYSQL_PORT = '4050'

else:
    MYSQL_DB = 'myweb_on_bae'
    MYSQL_USER = 'root'
    MYSQL_PASS = 'c1314520'
    MYSQL_HOST_M = '127.0.0.1'
    MYSQL_HOST_S = '127.0.0.1'
    MYSQL_PORT = '3306'

# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'esp8266.apps.Esp8266AppConfig',
    'blog',
    'weichat',
    'pagination',
    'rest_framework',
    'snippets',
    'myhome.apps.MyhomeAppConfig',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'myweb.urls'

WSGI_APPLICATION = 'myweb.wsgi.application'
LOGIN_REDIRECT_URL = '/blog/'

# TEMPLATE_DIRS
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'myweb/templates'),
)


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DB,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST': MYSQL_HOST_M,
        'PORT': MYSQL_PORT,
    },
    'myweb_bak': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myweb_bak',
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST': MYSQL_HOST_M,
        'PORT': MYSQL_PORT,

    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh_cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

MEDIA_URL = '/media/'

STATIC_URL = '/static/'
if 'SERVER_SOFTWARE' in os.environ:  # BAE
    STATIC_ROOT = 'static'
    STATICFILES_DIRS = (
        '',
    )
else:
    STATIC_ROOT = ''
    STATICFILES_DIRS = (
        'static',
    )

if 'SERVER_SOFTWARE' in os.environ:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': "redis://[:'dce9b62692b7446391f52cca2840784e-86558724fa9d48ab91a5283a2bb3d061-ZuriHfOCGBOrvQjfMlZJ']@redis.duapp.com:80",
            'OPTIONS': {
                #'DB':'ZuriHfOCGBOrvQjfMlZJ',
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                #'USERNAME': '13bcc102c85f4247bc63c9a0c1cc8b16',
                #'PASSWORD': 'dce9b62692b7446391f52cca2840784e-86558724fa9d48ab91a5283a2bb3d061-ZuriHfOCGBOrvQjfMlZJ',
                #'PICKLE_VERSION':-1,
                #'SOCKET_TIMEOUT':60,
                #'IGNORE_EXCEPTIONS':True,

            }
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379:0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
# REST_FRAMEWORK = {
#   'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
#}
