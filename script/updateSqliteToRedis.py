#!/root/deliverkindle.com/bin/python
# -*- coding: utf-8 -*- 

import sqlite3
import MySQLdb
import redis
import esclient
import json
import re
from os import path
import ConfigParser 
import struct
import socket
import sys
import datetime
import time

#access deliverkindle model
import sys, os.path 
sys.path.append("/home/data/www.deliverkindle.com")
#export DJANGO_SETTINGS_MODULE=deliverkindle.settings
from deliverkindle.settings import *
from deliverkindle.books.models import Series, BooksAdd
from django.db import connections

cf                        = ConfigParser.ConfigParser()
cf.read("config.conf")

CALIBRE_ALL_BOOKS_SET              = cf.get("key", "CALIBRE_ALL_BOOKS_SET")
CALIBRE_ALL_BOOKS_HASH             = cf.get("key", "CALIBRE_ALL_BOOKS_HASH")

CALIBRE_ALL_SERIES_SET             = cf.get("key", "CALIBRE_ALL_SERIES_SET")
CALIBRE_ALL_SERIES_HASH            = cf.get("key", "CALIBRE_ALL_SERIES_HASH")
CALIBRE_SERIES_BOOKS_HASH          = cf.get("key", "CALIBRE_SERIES_BOOKS_HASH")

CALIBRE_ALL_BOOKS_OBJ_HASH         = cf.get("key", "CALIBRE_ALL_BOOKS_OBJ_HASH")
CALIBRE_ALL_USER_BOOKS_HASH        = cf.get("key", "CALIBRE_ALL_USER_BOOKS_HASH")
CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET = cf.get("key", "CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET")
BOOK_LIBRARY                       = cf.get("path", "BOOK_LIBRARY")
REDIS_DB                           = cf.get("key", "REDIS_DB")
CALIBRE_ALL_BOOK_SERIES_HASH       = cf.get("key", "CALIBRE_ALL_BOOK_SERIES_HASH")
REDIS_DB                           = cf.get("key", "REDIS_DB")
CALIBRE_ALL_BOOKS_ID_TIMESTAMP_TUSHU_SET       = cf.get("key", "CALIBRE_ALL_BOOKS_ID_TIMESTAMP_TUSHU_SET")

fmt = "%Y-%m-%d %H:%M:%S"


repository       =  cf.get("path", "repository")
pool             = redis.ConnectionPool(host='127.0.0.1', port=6379, db=REDIS_DB, password='qazwsxedc')  
r                = redis.Redis(connection_pool=pool)
es               = esclient.ESClient("http://localhost:9200/")
conn             = sqlite3.connect(repository)
conn.row_factory = sqlite3.Row
cur              = conn.cursor()


#import MySQLdb
DataName = 'slave'
cursor = connections[DataName].cursor()
cursor.execute('drop view if exists booksplus')
sql = 'create view if not exists booksplus as select books.id,data.name,group_concat(distinct data.format) as format,data.uncompressed_size,\
		title,timestamp,pubdate, isbn ,path,uuid, has_cover, text as descript,author_sort as author from (books left join data on \
		books.id = data.book) left join comments on books.id = comments.book group by books.id'
cursor.execute(sql)

def getSeriesClick():
	try:
	    global cur
	    cur.execute('select id,click from series_id_click')
	    rows             = cur.fetchall()
	    id_click_dict    = {}
	    for row in rows:
		id_click_dict[row[0]] = row[1]
	    return id_click_dict
	except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
     	    return {}

def getBooksClick():
	try:
	    global cur
	    cur.execute('select id,click from booksplus_id_click')
	    rows             = cur.fetchall()
	    id_click_dict    = {}
	    for row in rows:
		id_click_dict[row[0]] = row[1]
	    return id_click_dict
	except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
	    return {}

def setUserFavorite():
	try:
	    global cur
	    cur.execute('select userid,group_concat(distinct bookid) as bookids from user_book_id group by userid;')
	    rows             = cur.fetchall()
	    id_favorite_dict    = {}
	    for row in rows:
	    	booklist = row['bookids'].split(",")
	    	handle_booklist  = map(int, booklist)
	    	handle_repeat_booklist = list(set(handle_booklist))
		r.hset(CALIBRE_ALL_USER_BOOKS_HASH, row['userid'],json.dumps(handle_repeat_booklist))
	except sqlite3.Error, e:
        	print "Error %s:" % e.args[0]

def get_index_dispaly_other_book():
	try:
		global cur
		new_list = map(str, INDEX_DISPLAY_CATE_ID.keys())
		sql      = 'select book,series from books_series_link where series in(' + ','.join(new_list) + ')'
		cur.execute(sql)
		book_series   = cur.fetchall()
		books = []
		for row in book_series:
			books.append(row['book'])
		return books
	except sqlite3.Error, e:
	    	print sql
        	print "Error %s:" % e.args[0]
        	return []


def getBookPath(id):
	global cur
	sql = 'select path from books where id=%s' % id
	cur.execute(sql)
	row = cur.fetchone()
	return "cover/" + row['path'] + "/cover_128_190.jpg" if row else "assets/images/cover_128_190.jpg"

if path.exists(repository):
	sql = 'select books.id,data.name,group_concat(distinct data.format) as format,data.uncompressed_size,\
		   title,timestamp,pubdate, isbn ,path,uuid, has_cover, text as descript,author_sort as author from (books left join data on \
		   books.id = data.book) left join comments on books.id = comments.book group by books.id order by timestamp desc'
	cur.execute(sql)
	rows = cur.fetchall()
	r.flushdb()
	es.delete_index("readream")
	id_click_books_dict = getBooksClick()
	id_click_series_dict = getSeriesClick()
	index_display_book_list = get_index_dispaly_other_book()
	print index_display_book_list
	setUserFavorite()
	#print rows
	for row in rows:
		#print row['timestamp'][:19]
		dt_obj = datetime.datetime.strptime(row['timestamp'][:19],fmt)
		time_tuple = dt_obj.timetuple()
		ts = time.mktime(time_tuple)

		click = id_click_books_dict[row['id']] if id_click_books_dict.has_key(row['id']) else 0

		r.hset(CALIBRE_ALL_BOOKS_HASH, row['id'], json.dumps(dict(row)))
		if row['id'] not in index_display_book_list:
			r.zadd(CALIBRE_ALL_BOOKS_ID_TIMESTAMP_TUSHU_SET,  row['id'], int(ts))
		r.zadd(CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET,  row['id'], int(ts))
		r.zadd(CALIBRE_ALL_BOOKS_SET,  row['id'], int(click))
		
		# index book
		data = dict(row)
		book_id = row['id']
		es.index("readream", "books", body=data, docid=book_id)
	import cPickle
	books_all_object = BooksAdd.objects.using('slave').all()
	for obj in books_all_object:
		r.hset(CALIBRE_ALL_BOOKS_OBJ_HASH, obj.id, cPickle.dumps(obj))

	sql  = 'select id, name from series'
	cur.execute(sql)
	rows = cur.fetchall()
	for row in rows:
		sql      = 'select book from books_series_link where series=%s order by book desc' % row['id']
		cur.execute(sql)
		books    = cur.fetchall()
		book_ids = [book['book'] for book in books]
		if len(book_ids)>0:
			first_id = book_ids[0]
			book_ids = map(str,book_ids)
			#path    = getBookPath(first_id)
			data     = {"id":row['id'], "name":row['name'],"count":len(book_ids)}

			click = int(id_click_series_dict[row['id']]) if id_click_series_dict.has_key(row['id']) else 0
			#print str(row['id']) + ":" + str(click)
			r.zadd(CALIBRE_ALL_SERIES_SET,  row['id'], int(click))
			r.hset(CALIBRE_ALL_SERIES_HASH, row['id'], json.dumps(data))
			r.hset(CALIBRE_SERIES_BOOKS_HASH, row['id'], json.dumps(book_ids))

	sql      = 'select book,series from books_series_link'
	cur.execute(sql)
	book_series   = cur.fetchall()
	for row in book_series:
		r.hset(CALIBRE_ALL_BOOK_SERIES_HASH,  row['book'], row['series'])


