# coding=utf-8
import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'i%0*1^gt6iy$)td%=z*87&4fJjj+x5g=04e&yu&72fr=2&m&vn'

MEDIA_URL = '/media/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',

)

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

ROOT_URLCONF = 'sms.urls'
WSGI_APPLICATION = 'sms.wsgi.application'

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATETIME_FORMAT = 'd/m/Y H:i'
TIME_FORMAT = 'H:i'
DATE_FORMAT = 'd/m/Y'
DATE_INPUT_FORMATS = ['%d/%m/%Y',]

STATIC_URL = '/static/'
DEBUG = False

if socket.gethostname() == 'chicosilva':
    DEBUG = True

TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG
FILER_DEBUG = DEBUG

ADMINS = (('seunome', 'seuemail@gmail.com'),)
MANAGERS = ADMINS

ALLOWED_HOSTS = ['.meudominio.com']

AUTH_USER_MODEL = 'autenticacao.CustomUser'


from config import *