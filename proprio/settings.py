"""
Django settings for proprio project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ov3sfsyj4*@0)m@3-j+m%%(0ms*et@d0hb+pl#6z2m(t=be*(n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# hack from http://stackoverflow.com/a/7651002/436792
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'main',
    'bank_import',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lineage',  # https://github.com/marcuswhybrow/django-lineage
    'bootstrapform',  # https://github.com/tzangms/django-bootstrap-form
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',  # for django-lineage
)
ROOT_URLCONF = 'proprio.urls'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data', 'db.sqlite3'),
    }
}

# uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, 'data', 'uploaded_files')
MEDIA_URL = '/files/'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (('fr', 'Francais'), ('de', 'Deutsch'), ('en', 'English'))
LANGUAGE_CODE = 'en_us'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = 'static'
STATIC_URL = '/static/'

PROPRIO_IMPORT_PARSERS = (
    "credit_agricole_bank_import.importer.importer",
)

# give the opportunity for the deployment script
# to override some of the settings
try:
    from additional_settings import *
except ImportError:
    pass
