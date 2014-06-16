#encoding:utf-8

#from settings import *
from django.conf.urls import *


urlpatterns = patterns('deliverkindle.books',
    (r'^$','views.books_list'),#列表页
    (r'^p(\d{1,10})/$','views.books_list'),#列表翻页
    # (r'^category/(\d+)/$','views.category_book_list'),#列表翻页
    # (r'^category/(\d+)/p(\d{1,10})/$','views.category_book_list'),#列表翻页
    (r'^(\d+)/$','views.books_detail'),#详细页面
    (r'^reader/(\d+)/(.*)$','views.open_book'),#详细页面
    (r'^search/$','views.search'),
    (r'^search/p(\d{1,10})/(.*)$','views.search'),
    (r'^mark/$','views.favorite_mark'),
    (r'^download/(\d{1,10})/(.*)$', 'views.download'),

)
