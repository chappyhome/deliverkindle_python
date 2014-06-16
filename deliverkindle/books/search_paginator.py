#encoding:utf-8

from django.core.paginator import Paginator

class _ListObjectList(object):
    """ List-backed list of results to paginate.
    """
    def __init__(self, es, q, index):
        self.es = es
        self.q = q
        self.index = index
        
    def __getslice__(self, start, stop):
    	keyword = self.q.encode('utf-8')
    	s = int(start)
    	p = int(stop)
    	query_string_args = {
                    "query": {"query_string":{"query":keyword}},
                    "sort":"_score",
                    "from":s,
                    "size":p - s
                    }

        #print query_string_args

        result = self.es.search(query_body=query_string_args,
                                    indexes=[self.index])
        books = result['hits']['hits']
        data = [book['_source'] for book in books]
        return data
        
    def count(self):
    	keyword = self.q.encode('utf-8')
        query_string_args = {
                    "query": {"query_string":{"query":keyword}},
                    }

        #print query_string_args

        result = self.es.search(query_body=query_string_args,
                                    indexes=[self.index])

        total = result['hits']['total']
        return int(total)

class BaseSearchPaginator(Paginator):
	def __init__(self, es, q, per_page, orphans=0, allow_empty_first_page=True,index="readream"):
	    object_list = _ListObjectList(es, q, index)
	    super(BaseSearchPaginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)

class SearchPaginator(BaseSearchPaginator):
    """ A paginator for Search list.
    """
    def __init__(self, *args, **kwargs):
        super(SearchPaginator, self).__init__(*args, **kwargs)