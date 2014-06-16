#encoding:utf-8

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
from deliverkindle.settings import *
from os import path, system
import datetime
import time
import json

class Series(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    name = models.TextField()
    sort = models.TextField(blank=True)
    class Meta:
        db_table = 'series'

class BooksAdd(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    format = models.TextField(blank=True, null=True)
    uncompressed_size = models.TextField(blank=True, null=True)
    title = models.TextField()
    timestamp = models.DateTimeField()
    pubdate = models.DateTimeField()
    isbn = models.TextField()
    path = models.TextField()
    uuid = models.TextField()
    has_cover = models.IntegerField()
    descript = models.TextField(blank=True, null=True)
    author = models.TextField()

    def get_absolute_url(self):
        return '/books/%d/' %int(self.id)
    class Meta:
        db_table = 'booksplus'

class Comments(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    book = models.TextField(unique=True, blank=True) # This field type is a guess.
    text = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        managed = False
        db_table = 'comments'

class SeriesIdClick(models.Model):
    id = models.IntegerField(primary_key=True,blank=True)
    click = models.IntegerField(blank=True)
    class Meta:
        managed = False
        db_table = 'series_id_click'

class UserBookId(models.Model):
    id = models.IntegerField(primary_key=True,blank=True)
    userid = models.IntegerField(blank=True)
    bookid = models.IntegerField(blank=True)
    class Meta:
        managed = False
        db_table = 'user_book_id'

class BooksplusIdClick(models.Model):
    id = models.IntegerField(primary_key=True,blank=True)
    click = models.IntegerField(blank=True)
    class Meta:
        managed = False
        db_table = 'booksplus_id_click'

class Publishers(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    name = models.TextField(unique=True)
    sort = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'publishers'

class Data(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    book = models.TextField(blank=True) # This field type is a guess.
    format = models.TextField(blank=True) # This field type is a guess.
    uncompressed_size = models.TextField(blank=True) # This field type is a guess.
    name = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        managed = False
        db_table = 'data'

class BooksSeriesLink(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    book = models.IntegerField(unique=True)
    series = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'books_series_link'

class Tags(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    name = models.TextField(unique=True)
    class Meta:
        managed = False
        db_table = 'tags'

class Books(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    title = models.TextField()
    sort = models.TextField(blank=True)
    timestamp = models.DateTimeField(blank=True) # This field type is a guess.
    pubdate = models.DateTimeField(blank=True) # This field type is a guess.
    series_index = models.FloatField()
    author_sort = models.TextField(blank=True)
    isbn = models.TextField(blank=True)
    lccn = models.TextField(blank=True)
    path = models.TextField()
    flags = models.IntegerField()
    uuid = models.TextField(blank=True)
    has_cover = models.NullBooleanField()
    last_modified = models.DateTimeField() # This field type is a guess.
    class Meta:
        db_table = 'books'

def callback_on_post_delete(sender,**kwargs):
    from deliverkindle.books.models import BooksSeriesLink
    book_id = kwargs['instance'].id
    book_path = kwargs['instance'].path
    del_dir = unzip_dir + book_path
    #delete redis data
    r.zrem(CALIBRE_ALL_BOOKS_SET, book_id)
    r.zrem(CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET, book_id)
    r.hdel(CALIBRE_ALL_BOOKS_HASH, book_id)
    #reset series
    series_obj = BooksSeriesLink.objects.filter(book=book_id)
    if series_obj:
        res = BooksSeriesLink.objects.filter(series=series_obj[0].series)
        book_ids = [obj.book for obj in res]
        r.hset(CALIBRE_SERIES_BOOKS_HASH, series_obj[0].series, json.dumps(book_ids))
    #delete es key
    es.delete("readream", "books", book_id)
    #delete file
    if unzip_dir in del_dir and len(del_dir) > len(unzip_dir) and path.exists(del_dir):
            system('rm -fr "' + del_dir + '"')

    #delete book from calibre
    # command = 'calibredb remove "{0}" --library-path {1}'.format(book_id,  BOOK_LIBRARY)
    # system(command)

def callback_on_post_save(sender,**kwargs):
    from django.forms.models import model_to_dict
    import cPickle
    book_id = kwargs['instance'].id
    timestamp = kwargs['instance'].timestamp
    pubdate = kwargs['instance'].pubdate
    last_modified = kwargs['instance'].last_modified
   
    #dt_obj = datetime.datetime.strptime(timestamp[:19],fmt)
    time_tuple = timestamp.timetuple()
    ts = time.mktime(time_tuple)
    tp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    pd = pubdate.strftime('%Y-%m-%d %H:%M:%S')
    lm = last_modified.strftime('%Y-%m-%d %H:%M:%S')

    books_object = BooksAdd.objects.get(id=book_id)
    #l = model_to_dict(books_object)
    books_object.timestamp = tp
    books_object.pubdate = pd
    books_object.last_modified = lm
    
    #add to redis and index to es
    r.hset(CALIBRE_ALL_BOOKS_OBJ_HASH, book_id, cPickle.dumps(books_object))
    r.hset(CALIBRE_ALL_BOOKS_HASH, book_id, json.dumps(model_to_dict(books_object)))
    r.zadd(CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET,  book_id, int(ts))
    r.zadd(CALIBRE_ALL_BOOKS_SET,  book_id, 0)

    data = model_to_dict(books_object)
    es.index("readream", "books", body=data, docid=book_id)

signals.post_delete.connect(callback_on_post_delete, sender=Books)
signals.post_save.connect(callback_on_post_save, sender=Books)
