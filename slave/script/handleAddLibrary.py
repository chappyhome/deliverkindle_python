#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import subprocess
import sqlite3
import redis
import pyinotify
import esclient
import re
import json
import datetime
import time
from os import path, system
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("config.conf")
repository                 =  cf.get("path", "repository")
dropbox_repository         =  cf.get("path", "dropbox_repository")
unzip_dir                  =  cf.get("path", "workDir")
BOOK_LIBRARY               =  cf.get("path", "BOOK_LIBRARY")
elasticsearch_host         =  cf.get("path", "elasticsearch_host")
synchronous_repository     =  cf.get("path", "synchronous_repository")


CALIBRE_ALL_BOOKS_SET  =  cf.get("key", "CALIBRE_ALL_BOOKS_SET")
CALIBRE_ALL_BOOKS_HASH =  cf.get("key", "CALIBRE_ALL_BOOKS_HASH")

CALIBRE_ALL_SERIES_SET     = cf.get("key", "CALIBRE_ALL_SERIES_SET")
CALIBRE_ALL_SERIES_HASH    = cf.get("key", "CALIBRE_ALL_SERIES_HASH")
CALIBRE_SERIES_BOOKS_HASH  = cf.get("key", "CALIBRE_SERIES_BOOKS_HASH")
CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET = cf.get("key", "CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET")
CALIBRE_ALL_BOOKS_OBJ_HASH = cf.get("key", "CALIBRE_ALL_BOOKS_OBJ_HASH")
TMP_BOOK_ID                = cf.get("key", "TMP_BOOK_ID")
REDIS_DB                   = cf.get("key", "REDIS_DB")

fmt = "%Y-%m-%d %H:%M:%S"

#init redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=REDIS_DB, password='qazwsxedc')
r = redis.Redis(connection_pool=pool)
#init sqlite3
conn = sqlite3.connect(repository)
conn.text_factory=str
conn.row_factory = sqlite3.Row
cur = conn.cursor()

#init es
es = esclient.ESClient(elasticsearch_host)

import sys, os.path 
sys.path.append("/data/htdocs/deliverkindle")
#export DJANGO_SETTINGS_MODULE=deliverkindle.settings
#from deliverkindle.settings import *
from deliverkindle.books.models import Series, BooksAdd


wm = pyinotify.WatchManager()

class EventHandler(pyinotify.ProcessEvent):

    def process_IN_CREATE(self, evt):
        print "create ", evt.pathname

    def process_IN_MOVED_TO(self, evt):
        print "IN_MOVED_TO ", evt.pathname
        ext = path.splitext(evt.pathname)[1]

	if ext == '.db':
	    book_id = r.get(TMP_BOOK_ID)
	    update_single_series_to_redis(book_id)
        if ext == '.epub':
            dir = path.dirname(evt.pathname)
            command = 'calibredb add -d "{0}" --library-path {1}'.format(dir,  BOOK_LIBRARY)
	    print command
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = p.stdout.readlines()
	    print out
            if len(out)>=3:
		pattern = re.compile('.*\s+(\d+)\\n$')
		match = pattern.match(out[1])
		fid = match.groups()[0]
		bookid = int(fid)
		print match.groups()[0]
		#sql = 'select * from books where id=%d' % bookid
		#sql = 'select books.id,title,timestamp,pubdate, isbn ,path,uuid, has_cover, text as desc,\
		#      author_sort as author from books left join comments on books.id = comments.book where books.id=%d' % bookid
		sql = 'select books.id,data.name,group_concat(distinct data.format) as format,data.uncompressed_size,\
		       title,timestamp,pubdate, isbn ,path,uuid, has_cover, text as descript,author_sort as author from (books left join data on \
		       books.id = data.book) left join comments on books.id = comments.book where books.id=%d group by books.id order by timestamp \
		       desc' % bookid
		cur.execute(sql)
		row = cur.fetchone()
		dt_obj = datetime.datetime.strptime(row['timestamp'][:19],fmt)
		time_tuple = dt_obj.timetuple()
		ts = time.mktime(time_tuple)
		#add to redis and index to es	
		r.hset(CALIBRE_ALL_BOOKS_HASH, row['id'], json.dumps(dict(row)))
		r.zadd(CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET,  row['id'], int(ts))
		r.zadd(CALIBRE_ALL_BOOKS_SET,  row['id'], 0)

		r.set(TMP_BOOK_ID, bookid)

		data = dict(row)
		book_id = row['id']
		print "index to es"
		es.index("readream", "books", body=data, docid=book_id)


		#unzip
		output = unzip_dir + row['path']
		mkdircommand = 'mkdir -p "%s"' % output
		if not path.exists(output):
			system(mkdircommand)
			command = 'unzip -o "{0}" -d  "{1}"'.format(evt.pathname, output)
			print command
			system(command)

		#convert cover to 128X190
		cover_path = unzip_dir + row['path'] + '/cover_128_190.jpg'
		if not path.isfile(cover_path):
			original = BOOK_LIBRARY + "/" + row['path'] + '/cover.jpg'
			command = 'convert -resize 128X190! "{0}"        "{1}"'.format(original, cover_path)
			print command
			system(command)

		#add new book obj to redis
		import cPickle
		books_object = BooksAdd.objects.get(id=book_id)
		r.hset(CALIBRE_ALL_BOOKS_OBJ_HASH, book_id, cPickle.dumps(books_object))
		#del data and dir
		del_sqlite_and_dir('books')
		#del_sqlite_and_dir('booksplus')



def del_sqlite_and_dir(table_name):
    try:
	global conn, cur, sqlite3, sys, unzip_dir, system, CALIBRE_ALL_BOOKS_HASH, CALIBRE_ALL_BOOKS_SET, r, es
	sql = 'select * from ' + table_name + ' \
	where title in (select  title  from  '+ table_name + '  group  by  title  having  count(title) > 1)'
	cur.execute(sql)
	rows = cur.fetchall()
	titles = [row['title'] for row in rows]
	no_zf_titles = set(titles)
	# print no_zf_titles
	id_del_list = []
	p_del_list = []
	for title in no_zf_titles:
		sql = 'select id,path from '+table_name+ ' where title="' + title + '"'
		cur.execute(sql)
		records = cur.fetchall()
		id_record = [str(record[0]) for record in records]
		p_record = [str(record[1]) for record in records]
		id_record.pop()
		p_record.pop()
		id_del_list += id_record
		p_del_list += p_record
		# r = []
	del_sql_books = 'delete from '+table_name+' where id in(' + ','.join(id_del_list) + ')'
	del_sql_data = 'delete from data where book in(' + ','.join(id_del_list) + ')'
	del_sql_comments = 'delete from comments where book in(' + ','.join(id_del_list) + ')'
	del_sql_series = 'delete from books_series_link where book in(' + ','.join(id_del_list) + ')'

	del_dir_list = [unzip_dir + item for item in p_del_list]
	# print del_dir_list
	#del sqlite
	cur.execute(del_sql_books)
	cur.execute(del_sql_data)
	cur.execute(del_sql_comments)
	cur.execute(del_sql_series)
	conn.commit()

	#del redis
	for id in id_del_list:
		r.zrem(CALIBRE_ALL_BOOKS_SET, id)
		r.zrem(CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET, id)
		r.hdel(CALIBRE_ALL_BOOKS_HASH, id)
		r.hdel(CALIBRE_ALL_BOOKS_OBJ_HASH, id)
		es.delete("readream", "books", id)
	#del dir
	for dir in del_dir_list:
		if unzip_dir in dir and len(dir) > len(unzip_dir) and path.exists(dir):
			system('rm -fr "' + dir + '"')
	print del_sql_data
	print id_del_list
	print p_del_list

	
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        #sys.exit(1)

def getBookPath(id):
	global cur
	sql = 'select path from books where id=%s' % id
	cur.execute(sql)
	row = cur.fetchone()
	return "cover/" + row['path'] + "/cover_128_190.jpg" if row else "assets/images/cover_128_190.jpg"

def getDropboxDbSeriesName():
	global sqlite3, dropbox_repository
	dropbox_conn = sqlite3.connect(dropbox_repository)
	dropbox_conn.row_factory = sqlite3.Row
	dropbox_cur = dropbox_conn.cursor()

	sql = 'select name from series order by id desc'
	dropbox_cur.execute(sql)
	series = dropbox_cur.fetchone()
	return  series['name']

def update_single_series_to_redis(book_id):
	try:
		global conn, cur, sqlite3, r, CALIBRE_ALL_SERIES_SET, CALIBRE_SERIES_BOOKS_HASH

		series_name = getDropboxDbSeriesName()
		sql = 'select id from series where name="%s"' % series_name.encode('utf-8')
		cur.execute(sql)
		series = cur.fetchone()
		print sql
		print series
		if series is not None and len(series)>0:
			print 'aaaa'
			series_id = series['id']
			sql = 'insert or replace  into books_series_link(book, series) values({0}, {1})'.format(book_id, series_id)
			cur.execute(sql)
		else:
			print 'bbbb'
			sql = 'insert or replace into series( name, sort) values( "{0}", "{1}")'.format(series_name.encode('utf-8'), series_name.encode('utf-8'))
			cur.execute(sql)
			series_id = cur.lastrowid
			sql = 'insert or replace into books_series_link(book, series) values({0}, {1})'.format(book_id, series_id)
			cur.execute(sql)
		conn.commit()
		sql = 'select book from books_series_link where series=%s' % series_id
		cur.execute(sql)
		books = cur.fetchall()
		book_ids = [book['book'] for book in books]
		print book_ids
		print "book id:" +  str(book_id) + "  series id:" +  str(series_id)
		if len(book_ids)>0:
			first_id = book_ids[0]
			path = getBookPath(first_id)
			data = {"id":series_id, "name":series_name,"path":path}
			#r.zadd(CALIBRE_ALL_SERIES_SET,  json.dumps(data), series_id)
			r.zadd(CALIBRE_ALL_SERIES_SET,  series_id, 0)
			r.hset(CALIBRE_ALL_SERIES_HASH, series_id, json.dumps(data))
			r.hset(CALIBRE_SERIES_BOOKS_HASH, series_id, json.dumps(book_ids))

	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
notifier = pyinotify.Notifier(wm, EventHandler())
mask = pyinotify.IN_MOVED_TO | pyinotify.IN_CREATE
watcher = wm.add_watch(synchronous_repository, mask, rec=True, auto_add=True)
notifier.loop()
