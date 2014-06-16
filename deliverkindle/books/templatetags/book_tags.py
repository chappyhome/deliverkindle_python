# -*- coding: utf-8 -*-

from deliverkindle.books.models import *
from django.template import Library
from deliverkindle.settings import *
import json
import cPickle
#import redis
#import esclient


#r = redis.Redis(host='127.0.0.1', db =1)
#es    = esclient.ESClient("http://localhost:9200/")
register = Library()


@register.inclusion_tag('book_category.tag.html')
def get_book_category():
    """
    得到图书分类
    """
    categorys_all = r.hgetall(CALIBRE_ALL_SERIES_HASH)
    
    categorys_values = categorys_all.values()
    #print categorys_all.values()
    #print categorys_values
    categorys_handle_values = map(json.loads, categorys_values)
    #print categorys_handle_values
    return {'categorys':categorys_handle_values}

#获取图书点击排行
@register.inclusion_tag('books_click.tag.html')
def get_book_by_clicktime(count=10): 
    try:
        entry_list = r.zrevrange(CALIBRE_ALL_BOOKS_SET, 0, count, withscores=True)
        # print entry_list
        bookid_click_dict = {}
        for bookid,click in entry_list:
            bookid_click_dict[int(bookid)] = int(click)
        #print bookid_click_dict
        bookids = [v[0] for v in entry_list]
        #print bookids
        books = r.hmget(CALIBRE_ALL_BOOKS_OBJ_HASH,bookids)
        json_books = map(cPickle.loads, books)

        data = []
        for book in json_books:
            click = bookid_click_dict[book.id]
            setattr(book,'click',click)
            data.append(book)
        #print data
        #data = map(json.loads, entry_list)
        #data = BooksAdd.objects.order_by('click')[0:10].get()
        #data =  BooksAdd.objects.order_by('-click')[0:count]

    except:
        data = {}
    return {'entry_list':data, 'bookid_click':bookid_click_dict}


#获取相近图书
@register.inclusion_tag('book_related.tag.html')
def get_book_by_related1(q, index="readream", count=10): 
    try:
        keyword = q.encode('utf-8')
        query_string_args = {
                    "query": {"query_string":{"query":keyword}},
                    "sort":"_score",
                    "from":0,
                    "size":10
                    }
        result = es.search(query_body=query_string_args,
                                    indexes=[index])


        books = result['hits']['hits']
        data = [book['_source'] for book in books]
        #print data



    except:
        data = {}
    result = data[1:] if data else {}
    return {'entry_list':result}

#获取类别点击排行
@register.inclusion_tag('book_click.category.html')
def get_category_by_clicktime(count=10): 
    try:
        entry_list = r.zrevrange(CALIBRE_ALL_SERIES_SET, 0, count, withscores=False)
        books = r.hmget(CALIBRE_ALL_SERIES_HASH,entry_list)
        data = map(json.loads, books)
    except:
        data = {}
    return {'entry_list':data}
