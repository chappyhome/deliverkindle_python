# -*- coding: utf-8 -*- 

import sys, os.path 
sys.path.append("/home/data/www.deliverkindle.com")
#export DJANGO_SETTINGS_MODULE=deliverkindle.settings
from deliverkindle.settings import *
from django.db import connections

import ConfigParser 
cf                        = ConfigParser.ConfigParser()
cf.read("config.conf")

CALIBRE_ALL_BOOKS_SET       = cf.get("key", "CALIBRE_ALL_BOOKS_SET")
CALIBRE_ALL_SERIES_SET      = cf.get("key", "CALIBRE_ALL_SERIES_SET")
CALIBRE_ALL_USER_BOOKS_HASH = cf.get("key", "CALIBRE_ALL_USER_BOOKS_HASH")
REDIS_DB                    = cf.get("key", "REDIS_DB")

import json
import redis
pool   = redis.ConnectionPool(host='127.0.0.1', port=6379, db=REDIS_DB)  
r      = redis.Redis(connection_pool=pool)



#import MySQLdb
DataName = 'slave'
cursor = connections[DataName].cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS booksplus_id_click(id integer PRIMARY KEY,click integer DEFAULT 0)')
cursor.execute('CREATE TABLE IF NOT EXISTS series_id_click(id integer PRIMARY KEY,click integer DEFAULT 0)')
cursor.execute('CREATE TABLE IF NOT EXISTS user_book_id(id integer PRIMARY KEY,userid integer,bookid integer)')

entry_list = r.zrevrange(CALIBRE_ALL_BOOKS_SET, 0, -1, withscores=True)
if entry_list is not None:
	for bookid,click in entry_list:
	    cursor.execute('insert or replace into booksplus_id_click(id, click) values(%d,%d)' % (int(bookid), int(click)))

entry_list = r.zrevrange(CALIBRE_ALL_SERIES_SET, 0, -1, withscores=True)
if entry_list is not None:
	for seriesid,click in entry_list:
	    cursor.execute('insert or replace into series_id_click(id, click) values(%d,%d)' % (int(seriesid), int(click)))

entry_list = r.hgetall(CALIBRE_ALL_USER_BOOKS_HASH)
#print entry_list
if entry_list is not None and len(entry_list)>0:
	for (key,value) in entry_list.items():
		value_list = json.loads(value)
		for bookid in value_list:
			cursor.execute('insert or replace into user_book_id(userid, bookid) values(%d,%d)' % (int(key), int(bookid)))
