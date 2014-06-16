# -*- coding: utf-8 -*-
#Copyright (C) 2011 Seán Hayes

from django.conf.urls.defaults import *

urlpatterns = patterns('deliverkindle.favorites',
	   (r'^collection/(\d+)/$','views.collection'),
	   (r'^delete/(\d+)/$','views.delete'),
)
