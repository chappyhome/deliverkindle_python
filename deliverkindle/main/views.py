#encoding:utf-8


from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render_to_response as render
from deliverkindle.books.models import BooksAdd
from django.template import RequestContext
from django.db.models import Count
from deliverkindle.topic.models import Topic
from deliverkindle.settings import *
import cPickle
import json
import datetime
import time
#from deliverkindle.books.models import BooksAdd
#from deliverkindle.favorites.models import MyFavorites
#import redis
#r = redis.Redis(host='127.0.0.1',db=1)



#@cache_page(60*60)
def index(request):
    current_page = 'index'
    page_title   = u'首页'
    current_timestamp = time.time()
    page_description = PAGE_DESCRIPT

    #最近评论
    topics       = Topic.objects.filter(deleted=False).order_by('-id')[0:16]
    #books        = BooksAdd.objects.order_by('-id')[0:20]

    #找到排除的书
    exclude_book_list = []
    for series in INDEX_DISPLAY_CATE_ID.keys():
        entry_list = r.hget(CALIBRE_SERIES_BOOKS_HASH, series)
        #print entry_list
        json_books = json.loads(entry_list)
        json_books_int = map(int, json_books)
        exclude_book_list += json_books_int


    #最新图书更新
    entry_list = r.zrevrange(CALIBRE_ALL_BOOKS_ID_TIMESTAMP_TUSHU_SET, 0, 21, withscores=True)
    bookid_click_dict = {}
    for bookid,timestamp in entry_list:
        bookid_click_dict[int(bookid)] = int(timestamp)
    bookids = [int(v[0]) for v in entry_list]


    rank_books = r.hmget(CALIBRE_ALL_BOOKS_OBJ_HASH,bookids)
    #print rank_books[:1]
    json_books = map(cPickle.loads, rank_books) if rank_books is not None else []
    books = []
    for book in json_books:
        timestamp = current_timestamp - bookid_click_dict[book.id]
        date = datetime.datetime.fromtimestamp(bookid_click_dict[book.id])
        setattr(book,'timestamp',timestamp)
        setattr(book,'date',date)
        if book.id not in exclude_book_list: #排除不想在这里显示的书
            books.append(book)


    #最新XXXXX更新
    output_display = {}
    index_display_cate_list = INDEX_DISPLAY_CATE_ID
    for key,values in INDEX_DISPLAY_CATE_ID.items():
        display_books = r.hget(CALIBRE_SERIES_BOOKS_HASH,key)
        json_display_books = json.loads(display_books) if display_books else []
        display_books_int = map(int, json_display_books)
        display_books_detail = r.hmget(CALIBRE_ALL_BOOKS_OBJ_HASH,display_books_int)
        json_display_books_detail = map(cPickle.loads, display_books_detail) if display_books_detail else []
        output_display_books = []
        output_display_detail = {}
        for book in json_display_books_detail[:22]:
            book_timestamp = to_timestamp(book.timestamp)
            timestamp = current_timestamp - book_timestamp
            date = datetime.datetime.fromtimestamp(book_timestamp)
            setattr(book,'timestamp',timestamp)
            setattr(book,'date',date)
            output_display_books.append(book)
        output_display_detail['books'] = output_display_books
        output_display_detail['dispaly_title'] = values
        output_display[key] = output_display_detail
    print output_display

    #排行榜
    entry_list = r.zrevrange(CALIBRE_ALL_BOOKS_SET, 0, 21, withscores=True)
    bookid_click_dict = {}
    for bookid,click in entry_list:
        bookid_click_dict[int(bookid)] = int(click)
    bookids = [v[0] for v in entry_list]
    rank_books = r.hmget(CALIBRE_ALL_BOOKS_OBJ_HASH,bookids)
    json_books = map(cPickle.loads, rank_books)
    datas = []
    for book in json_books:
        book.click = bookid_click_dict[book.id]
        datas.append(book)

    #热门标签
    try:
        entry_list = r.zrevrange(CALIBRE_ALL_SERIES_SET, 0, 30, withscores=False)
        print entry_list
        category_books = r.hmget(CALIBRE_ALL_SERIES_HASH,entry_list)
        categorys = map(json.loads, category_books)
    except:
        categorys = {}

    return render('index.html',locals(),context_instance=RequestContext(request))

def to_timestamp(timestamp):
    fmt = "%Y-%m-%d %H:%M:%S"
    try:
        dt_obj = datetime.datetime.strptime(timestamp[:19],fmt)
        time_tuple = dt_obj.timetuple()
    except:
        time_tuple = timestamp.timetuple()
    ts = time.mktime(time_tuple)
    return ts

def usernav(request):
    return render('user.nav.html',locals(),context_instance=RequestContext(request))

def about(request):
	return render('main_about.html',locals(),context_instance=RequestContext(request))
def disclaimer(request):
	return render('main_disclaimer.html',locals(),context_instance=RequestContext(request))

def contact(request):
	return render('main_contact.html',locals(),context_instance=RequestContext(request))

def partner(request):
	return render('main_partner.html',locals(),context_instance=RequestContext(request))

def subscribe(request):
	current_page = 'subscribe'
	return render('main_subscribe.html',locals(),context_instance=RequestContext(request))
