#encoding:utf-8

from django.core.paginator import Paginator
import json
#import redis
#r     = redis.Redis(host='127.0.0.1', db=1)
from deliverkindle.settings import r

class _ListObjectList(object):
    """ List-backed list of results to paginate.
    """
    def __init__(self, userid):
        self.userid = userid

    def __getslice__(self, start, stop):
        booklist_str = r.hget('calibre_all_user_books_hash', self.userid)
        booklist = json.loads(booklist_str) if booklist_str is not None else []
        if  booklist:
            books = r.hmget('calibre_all_books_hash',booklist[start:stop])
            data = map(json.loads, books) if books is not None else {}
        else:
            data = {}
        return data
        
    def count(self):
        booklist_str = r.hget('calibre_all_user_books_hash', self.userid)
        booklist = json.loads(booklist_str) if booklist_str is not None else []
        return len(booklist)

class BaseFavoritePaginator(Paginator):
	def __init__(self, userid, per_page, orphans=0, allow_empty_first_page=True):
	    object_list = _ListObjectList(userid)
	    super(BaseFavoritePaginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)

class FavoritePaginator(BaseFavoritePaginator):
    """ A paginator for Favorite list.
    """
    def __init__(self, *args, **kwargs):
        super(FavoritePaginator, self).__init__(*args, **kwargs)