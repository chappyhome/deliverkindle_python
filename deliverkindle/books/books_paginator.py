#encoding:utf-8

from django.core.paginator import Paginator
from deliverkindle.settings import *
import cPickle
import json
#import redis
#r     = redis.Redis(host='127.0.0.1')

class _ListObjectList(object):
    """ List-backed list of results to paginate.
    """
    def __getslice__(self, start, stop):
        entry_list = r.zrevrange(CALIBRE_ALL_BOOKS_ID_TIMESTAMP_SET, start, stop, withscores=False)
        books = r.hmget(CALIBRE_ALL_BOOKS_OBJ_HASH,entry_list)
        data = map(cPickle.loads, books)

        return data
        
    def count(self):
        return r.zcard(CALIBRE_ALL_BOOKS_SET)

class BaseSearchPaginator(Paginator):
	def __init__(self, per_page, orphans=0, allow_empty_first_page=True):
	    object_list = _ListObjectList()
	    super(BaseSearchPaginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)

class BooksPaginator(BaseSearchPaginator):
    """ A paginator for Search list.
    """
    def __init__(self, *args, **kwargs):
        super(BooksPaginator, self).__init__(*args, **kwargs)