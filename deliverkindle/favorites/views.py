# -*- coding: utf-8 -*-
#Copyright (C) 2013  David

#Python imports
from datetime import datetime
import logging

#Django imports
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from models import MyFavorites
logger = logging.getLogger(__name__)

@login_required
def collection(request,book_id):
    user_id = request.user.id
    try:
        # obj, created = MyFavorites.objects.get_or_create(user_id=user_id, book_id=book_id)
        # msg = '{"is_exists":false}' if created else '{"is_exists":true}'
        try:
            MyFavorites.objects.get(user_id=user_id, book_id=book_id)
            return HttpResponse('{"is_exists":true}', mimetype="text/plain")
        except MyFavorites.DoesNotExist:
            MyFavorites.objects.create(user_id=user_id, book_id=book_id)
            return HttpResponse('{"is_exists":false}', mimetype="text/plain")
    except Exception as e:
        print e
        error_msg = 'Bad Request or Handling Exceptions'
        return HttpResponseBadRequest(error_msg, mimetype="text/plain")

def delete(request,book_id):
    user_id = request.user.id
    try:
    	MyFavorites.objects.get(book_id=book_id,user_id=user_id).delete()
    	return HttpResponse('', mimetype="text/plain")
    except:
        error_msg = 'Bad Request or Handling Exceptions'
        return HttpResponseBadRequest(error_msg, mimetype="text/plain")





