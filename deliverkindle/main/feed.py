# -*- coding: utf-8 -*-

#from deliverkindle.books.models import BooksAdd
from django.contrib.syndication.views import Feed
from deliverkindle.settings import SITE_NAME, DOMAIN, CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET,CALIBRE_ALL_BOOKS_OBJ_HASH, r
import json
import cPickle

class BookFeed(Feed):
    title = '{0}最新图书'.format(SITE_NAME)
    link = '/feed/books.xml'


    def items(self):
        #return BooksAdd.objects.order_by('-id')[0:10]
        entry_list = r.zrevrange(CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET, 0, 10, withscores=False)
        print entry_list
        rank_books = r.hmget(CALIBRE_ALL_BOOKS_OBJ_HASH,entry_list)
        return map(cPickle.loads, rank_books)


    def item_title(self, item):
        return item.title + '-deliverkindle.com'

    def item_description(self, item):
    	return item.descript

    def item_link(self, item):
        #return item.get_absolute_url()
        return DOMAIN + '/books/%d/' %int(item.id)
