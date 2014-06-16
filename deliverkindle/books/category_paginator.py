#encoding:utf-8

from django.core.paginator import Paginator
from deliverkindle.settings import *
#import redis
import cPickle
import json

#r     = redis.Redis(host='127.0.0.1', db = 1)

class _ListObjectList(object):
    """ List-backed list of results to paginate.
    """
    def __init__(self, cateid):
        self.cateid = cateid
        
    def __getslice__(self, start, stop):
        book_ids_str = r.hget(CALIBRE_SERIES_BOOKS_HASH,self.cateid)
        book_ids = json.loads(book_ids_str) if book_ids_str is not None else []
        books = r.hmget(CALIBRE_ALL_BOOKS_OBJ_HASH,book_ids[start:stop])
        data = map(cPickle.loads, books)

        return data
        
    def count(self):
    	book_ids_str = r.hget(CALIBRE_SERIES_BOOKS_HASH,self.cateid)
        book_ids = json.loads(book_ids_str) if book_ids_str  is not None else []
        return len(book_ids)

class BaseSearchPaginator(Paginator):
	def __init__(self, cateid, per_page, orphans=0, allow_empty_first_page=True):
	    object_list = _ListObjectList(cateid)
	    super(BaseSearchPaginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)

class CategoryPaginator(BaseSearchPaginator):
    """ A paginator for Search list.
    """
    def __init__(self, *args, **kwargs):
        super(CategoryPaginator, self).__init__(*args, **kwargs)