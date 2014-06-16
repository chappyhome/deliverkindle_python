import sys, os.path 
sys.path.append("/home/data/www.deliverkindle.com")
#export DJANGO_SETTINGS_MODULE=deliverkindle.settings
from deliverkindle.settings import *
from deliverkindle.books.models import Series, BooksAdd
from deliverkindle.favorites.models import MyFavorites
from django.core.management import *
from django.db import connections
import json

import redis
pool   = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)  
r      = redis.Redis(connection_pool=pool)

import ConfigParser 
cf                        = ConfigParser.ConfigParser()
cf.read("config.conf")

CALIBRE_ALL_BOOKS_SET       = cf.get("key", "CALIBRE_ALL_BOOKS_SET")
CALIBRE_ALL_SERIES_SET      = cf.get("key", "CALIBRE_ALL_SERIES_SET")
CALIBRE_ALL_USER_BOOKS_HASH = cf.get("key", "CALIBRE_ALL_USER_BOOKS_HASH")

r.hset(CALIBRE_ALL_USER_BOOKS_HASH,1,json.dumps([]))
r.hset(CALIBRE_ALL_USER_BOOKS_HASH,2,json.dumps([]))

DataName = 'slave'
cursor = connections[DataName].cursor()
entry_list = r.hgetall(CALIBRE_ALL_USER_BOOKS_HASH)
print entry_list
