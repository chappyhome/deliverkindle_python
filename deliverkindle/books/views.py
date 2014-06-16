#encoding:utf-8

from django.http import HttpResponse,HttpResponseRedirect,Http404, HttpResponseBadRequest, HttpResponseNotAllowed
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from deliverkindle.books.models import *
from django.contrib import messages
from django.utils.encoding import smart_str
from django.utils.http import urlquote
#from zato.redis_paginator import ZSetPaginator
from deliverkindle.favorites.models import MyFavorites
from django.conf import settings
from forms import *
import json
import cPickle
import hashlib

from books_paginator import BooksPaginator
from search_paginator import SearchPaginator
from category_paginator import CategoryPaginator

# import esclient
# import redis
# r     = redis.Redis(host='127.0.0.1',db=1)
# es    = esclient.ESClient("http://localhost:9200/")
from deliverkindle.settings import *
RECENTVIEWE = 'recent_views'

def books_list(request,page=1):
    request.breadcrumbs([(u"图书列表",'/') 
                          ])
    current_page = 'books'
    pre_url = 'books'
    page_title = u'图书列表'
    form = SearchForm(request.POST)
    slave_domain = SLAVE_DOMAIN
    # book_all = BooksAdd.objects.all()
    # paginator = Paginator(book_all,10)
    #paginator = ZSetPaginator(r, 'calibre_all_books_sort_set', 10)
    paginator = BooksPaginator(10)
    allow_category = True
    not_allow_click_rank = False
    try:

        entrys = paginator.page(page)
    except (EmptyPage,InvalidPage):
        entrys = paginator.page(paginator.num_pages)

    #data = map(json.loads, entrys.object_list)
    #entrys.object_list = sorted(data)

    return render('books_list.html',locals(),context_instance=RequestContext(request,{'user':request.user}))


def category_list(request):
    current_page = 'category'
    request.breadcrumbs([(u"首页",'/'),  
                         (u"图书标签",'/category')  
                         ])

    return render('category_list.html',locals(),context_instance=RequestContext(request,{'user':request.user}))


def category_book_list(request, cateid, page=1):
    form = SearchForm(request.POST)
    current_page = 'category_list'
    pre_url = 'category/' + cateid

    page_title = u'图书标签'

    str = r.hget(CALIBRE_ALL_SERIES_HASH, cateid)
    if str is None:
        return render('404.html',locals(),context_instance=RequestContext(request,{'user':request.user}))
    hash = json.loads(str)
    page_description = hash['name']
    request.breadcrumbs([(u"首页",'/'),  
                         (u"图书标签",'/category'),
                         (hash['name'],'/category/' + cateid)
                         ])
    paginator = CategoryPaginator(cateid, 10)

    #add book click
    r.zincrby(CALIBRE_ALL_SERIES_SET, cateid, 1)
    # obj = Series.objects.get(id=cateid)
    # obj.click+=1
    # obj.save()
    ###############################################
    allow_category = True
    try:

        entrys = paginator.page(page)
    except (EmptyPage,InvalidPage):
        entrys = paginator.page(paginator.num_pages)

    return render('books_list.html',locals(),context_instance=RequestContext(request,{'user':request.user}))


def books_detail(request,book_id):  #calibre_all_books_hash
    current_page = 'book_detail'
    slave_domain = SLAVE_DOMAIN
    #book = BooksAdd.objects.get(id=book_id)
    str = r.hget(CALIBRE_ALL_BOOKS_OBJ_HASH, book_id)
    if str is None:
        return render('404.html',locals(),context_instance=RequestContext(request,{'user':request.user}))

    book = cPickle.loads(str)
    page_title = book.title
    page_description = book.descript

    book_cate_id = r.hget(CALIBRE_ALL_BOOK_SERIES_HASH, book_id)
    print book_cate_id
    book_cate_info = r.hget(CALIBRE_ALL_SERIES_HASH, book_cate_id)
    book_cate_info_json = json.loads(book_cate_info) if book_cate_info else {}
   
    # format = list(set(book.format.split(",")))
    # book.format = " ".join(format) if format else ""
    format_list = book.format.split(",") if book.format else []

    open_format_list = []
    for format in format_list:
        if format.lower() == 'pdf':
            open_format_list.append('PDF')
        elif format.lower() == 'epub':
            open_format_list.append('EPUB')

    url =   slave_domain + "/static/download/" + book.path + "/" + book.name
    key = hashlib.md5()
    key.update(DOWNLOAD_SLAVE_PASSWORD + request.META['REMOTE_ADDR'])
    ipkey = key.hexdigest()

    if not request.user.id:
        is_favorite = False
    else:
        booklist_str = r.hget(CALIBRE_ALL_USER_BOOKS_HASH, request.user.id)
        booklist = json.loads(booklist_str) if booklist_str is not None else []
        bookid = int(book_id)
        if bookid not in booklist:
            is_favorite = False
        else:
            is_favorite = True

    


    # print book.pubdate
    return render('book_detail.html',locals(),context_instance=RequestContext(request,{'user':request.user}))
def download(request, book_id, format):
    slave_domain = SLAVE_DOMAIN
    #book = BooksAdd.objects.get(id=book_id)
    str = r.hget(CALIBRE_ALL_BOOKS_OBJ_HASH, book_id)
    if str is None:
        return render('404.html',locals(),context_instance=RequestContext(request,{'user':request.user}))
    book = cPickle.loads(str)
    file_name = book.name + "." + format.lower()
    url =   slave_domain + "/static/download/" + book.path + "/" + file_name
    import urllib
    print urllib.quote_plus(url)
    response = HttpResponse(mimetype='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name
    response['X-Sendfile'] = smart_str(url)
    return response



def open_book(request,book_id,file_type):  #calibre_all_books_hash
    str = r.hget(CALIBRE_ALL_BOOKS_OBJ_HASH, book_id)
    if str is None:
        return render('404.html',locals(),context_instance=RequestContext(request,{'user':request.user}))
    book = cPickle.loads(str)
    epub_path = '/static/epub_content/' + book.path + "/"
    pdf_path = '/static/epub_content/' + book.path + "/" + book.name + '.pdf'
    #path = epub_path if file_type == 'epub' else pdf_path
    reader = 'reader.html' if file_type == 'epub' else 'reader_pdf.html'

    #add book click
    r.zincrby(CALIBRE_ALL_BOOKS_SET, book_id, 1)

    ###############################################

    
    return render(reader,locals(),context_instance=RequestContext(request,{'user':request.user}))



def search(request,page=1, q = ''):
    current_page = 'search'
    keyword = request.GET['q'] if not q else q
    form = SearchForm(request.GET)
    pre_url = 'books/search'
    no_display_paginator_breadcrumbs = True
    not_allow_click_rank = True
    if form.is_valid():
        #data = form.cleaned_data
        keyword = request.GET['q'] if not q else q
        suf_url = keyword
        try:
            paginator = SearchPaginator(es, keyword, 10, index="readream")
            allow_category = True
            try:

                entrys = paginator.page(page)
            except (EmptyPage,InvalidPage):
                entrys = paginator.page(paginator.num_pages)

            return render('books_list.html',locals(),context_instance=RequestContext(request,{'user':request.user}))
        except:
            entrys = []
            return render('books_list.html',locals(),context_instance=RequestContext(request,{'user':request.user}))

def favorite_mark(request):
    """
    添加收藏(ajax方式)
    """

    # 判断数据提交方式
    if request.method == 'GET':
        return HttpResponseRedirect('/')

    # 验证用户是否登录
    if not request.user.id:
        return HttpResponse( '{"status":-1}', mimetype="text/plain")

    # 验证图书是否存在
    book_id = int(request.POST.get('book_id'))
    book = r.hget(CALIBRE_ALL_BOOKS_OBJ_HASH, book_id)
    if book is None:
        return HttpResponse( '{"status":0}', mimetype="text/plain")


    booklist_str = r.hget(CALIBRE_ALL_USER_BOOKS_HASH, request.user.id)
    booklist = json.loads(booklist_str) if booklist_str is not None else []
    if book_id not in booklist:
        booklist.append(book_id)
        r.hset(CALIBRE_ALL_USER_BOOKS_HASH, request.user.id, json.dumps(booklist))
        return HttpResponse('{"status":1,"info":"Marked"}', mimetype="text/plain")
    else:
        remove_booklist = filter(lambda x: x != book_id, booklist)
        r.hset(CALIBRE_ALL_USER_BOOKS_HASH, request.user.id, json.dumps(remove_booklist))
        return HttpResponse('{"status":1,"info":"+ Mark"}', mimetype="text/plain")



