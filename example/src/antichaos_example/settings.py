# -*- coding: utf-8 -*-
import os
import os.path

PROJECT_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = (PROJECT_ROOT=='.') and os.getcwd() or PROJECT_ROOT

from django.utils.translation import ugettext_lazy as _

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'antichaos-example.sqlite'
DATABASE_USER = 'db_user'
DATABASE_PASSWORD = 'db_pass'
DATABASE_HOST = ''
DATABASE_PORT = ''

DEFAULT_CHARSET = 'UTF-8'

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'en'
DEFAULT_LANGUAGE = 1
LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = os.path.normpath(os.path.join(PROJECT_ROOT, 'media'))
MEDIA_URL = 'http://127.0.0.1:8000/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = 'JGP&*(j9fLK*(uiJO&*(h962L*^&*^%&*h68IY*igh$^jIK(<M'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'antichaos_example.urls'

TEMPLATE_DIRS = (
    os.path.normpath(os.path.join(PROJECT_ROOT, 'tempates')),
)

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.admin',
    'tagging',
    'django_antichaos',
    'antichaos_example',
)

EMAIL_SUBJECT_PREFIX = ''
SERVER_EMAIL = 'noreply@localhost'

try:
    from local_settings import *
except ImportError:
    pass

import logging
logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)d: %(message)s')

