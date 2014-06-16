"""
Django settings for deliverkindle project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import redis
import esclient
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '13kp0#t(e=y49op1x#0yx914pbi8brm!w!m*ue-34emifdr&bo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'deliverkindle',
    'deliverkindle.books',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'deliverkindle.urls'

WSGI_APPLICATION = 'deliverkindle.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/chappyhome/NEWBOOK/metadata.db',
    }
}

r     = redis.Redis(host='127.0.0.1', db = 0, password='qazwsxedc')
es    = esclient.ESClient("http://59.188.87.61:9200/")

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


#redis key value
CALIBRE_ALL_BOOKS_SET              = 'calibre_all_books_sort_set'
CALIBRE_ALL_BOOKS_HASH             = 'calibre_all_books_hash'
CALIBRE_ALL_BOOKS_LIST             = 'calibre_all_books_list'
CALIBRE_ALL_SERIES_SET             = 'calibre_all_series_set'
CALIBRE_ALL_SERIES_HASH            = 'calibre_all_series_hash'
CALIBRE_SERIES_BOOKS_HASH          = 'calibre_series_books_hash'
CALIBRE_ALL_BOOKS_OBJ_HASH         = 'calibre_all_books_obj_hash'
CALIBRE_ALL_USER_BOOKS_HASH        = 'calibre_all_user_books_hash'
CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET = 'calibre_all_books_id_timestamp_set'
unzip_dir                          =  '/data/htdocs/static/epub_content/'
BOOK_LIBRARY                       =  '/home/chappyhome/NEWBOOK'
