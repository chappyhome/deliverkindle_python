# -*- coding: utf-8 -*-
# Django settings for deliverkindle project.
import os
import sys
import redis
import esclient


ROOT_PATH = os.path.normpath(os.path.dirname(__file__)).replace('\\','/')
DEFAULT_CHARSET = 'utf8'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_NAME = '梦想读书家园'
PAGE_DESCRIPT = '本网站收集网络的图书,免费提供在线图书阅读下载平台,包括各种网络小说,畅销图书,村上春树,人物传记类等,IT技术图书,格式包括,pdf,chm,epub,mobi等'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'slave': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/home/data/NEWBOOK/metadata.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                     # Set to empty string for default.
    },

    'test': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'qazwsxedc2013',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                     # Set to empty string for default.
    },
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'deliverkindle',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'qazwsxedc2013',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                     # Set to empty string for default.
    },
}

r     = redis.Redis(host='127.0.0.1', db = 0, password='qazwsxedc')
es    = esclient.ESClient("http://localhost:9200/")

#r = redis.Redis(host='127.0.0.1')
DOMAIN = 'http://www.deliverkindle.com'
SLAVE_DOMAIN = 'http://download.deliverkindle.com'
DOWNLOAD_SLAVE_PASSWORD = '9321hhdtrsuwy267ddt'

INDEX_DISPLAY_CATE_ID = {206:'最新名博更新', 
                           4:'最新网络小说更新', 
                          33:'最新科幻玄幻更新'}



# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(ROOT_PATH,'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/data/www.deliverkindle.com/deliverkindle/staitc',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^n%+5xc_o8v&w0ua4&%q1gv^5+hl#8(=z4%#y@o$iyk)qe_1t*'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'breadcrumbs.middleware.BreadcrumbsMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'deliverkindle.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'deliverkindle.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH,'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.comments',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'deliverkindle.books',
    'deliverkindle.main',
    'deliverkindle.accounts',
    'deliverkindle.main',
    'deliverkindle.favorites',
    'deliverkindle.home',
    'deliverkindle.topic',
    #'django_basic_feedback',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

AUTH_PROFILE_MODULE                = 'accounts.UserProfile'

SESSION_SERIALIZER                 = 'django.contrib.sessions.serializers.JSONSerializer'


EMAIL_USE_TLS                      = True
EMAIL_HOST                         = 'smtp.gmail.com'
EMAIL_HOST_USER                    = 'pengboyun2013@gmail.com'
EMAIL_HOST_PASSWORD                = 'qazwsxedc2013'
EMAIL_PORT                         = 587

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
CALIBRE_ALL_BOOKS_ID_TIMESTAMP_TUSHU_SET = 'calibre_all_books_id_timestamp_tushu_set'
CALIBRE_ALL_BOOK_SERIES_HASH       = 'calibre_all_book_series_hash'

unzip_dir                          =  '/home/data/www.deliverkindle.com_product/deliverkindle/staitc/epub_content/'
BOOK_LIBRARY                       =  '/home/data/NEWBOOK'

DOUBAN_API_KEY                     = '' 
DOUBAN_API_SECRET                  = '' 
DOUBAN_SCOPE                       = 'shuo_basic_r,shuo_basic_w,douban_basic_common' 
DOUBAN_CALLBACK_URL                = u'http://pythoner.net/accounts/login/douban/callback/'

WEIBO_APP_KEY                      = u''
WEIBO_APP_SECRET                   = u''
WEIBO_CALLBACK_URL                 = u'http://pythoner.net/accounts/login/sina/callback/'
