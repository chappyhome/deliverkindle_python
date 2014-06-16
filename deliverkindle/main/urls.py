#encoding:utf-8


from django.conf.urls import *

urlpatterns = patterns('deliverkindle.main',
    (r'^usernav/$','views.usernav'),
)
