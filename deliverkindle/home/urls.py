#encoding:utf-8

from django.conf.urls import *

urlpatterns = patterns('deliverkindle.home',
    (r'^$','views.bookshelf'),
    (r'^p(\d{1,10})/$','views.bookshelf'),
    (r'^(\d{1,10})/$','profile.index'),
    (r'^(\d{1,10})/p(\d{1,10})/$','profile.index'),
    (r'^(\d{1,10})/follow/$','relation.follow'),
    (r'^(\d{1,10})/follows/$','relation.follows'),
    (r'^(\d{1,10})/fans/$','relation.fans'),

    (r'^bookshelf/$','views.bookshelf'),
    (r'^bookshelf/p(\d{1,10})/$','views.bookshelf'),

    (r'^(\d{1,10})/topic/$','views.topic'),
    (r'^(\d{1,10})/topic/p(\d{1,10})/$','views.topic'),

    (r'^download/','views.download'),
    (r'^download/p(\d{1,10})/$','views.download'),

    (r'^edit/$','profile.edit'),
    (r'^delete/$','profile.delete'),
    (r'^password/$','profile.password'),
    (r'^photo/$','profile.photo'),
    (r'^link/$','profile.link'),
    (r'^city/$','city.index'),
    (r'^members/$','views.members'),
    (r'^members/p(\d{1,10})/$','views.members'),
)
