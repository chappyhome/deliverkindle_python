# -*- coding: utf-8 -*-
#Copyright (C) 2013 David

#Python imports
from django.contrib.auth.models import User
from deliverkindle.books.models import BooksAdd
from django.db import models

# class MyFavorites1(models.Model):
#     id = models.IntegerField(primary_key=True)
#     user = models.ForeignKey(User,unique=True)
#     user_id = models.IntegerField()
#     book_id = models.IntegerField()
#     click = models.IntegerField()
#     class Meta:
#         db_table = 'my_favorites'

class MyFavorites(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    book = models.ForeignKey(BooksAdd)
    c_timestamp = models.DateTimeField('时间',auto_now_add=True)
    class Meta:
        db_table = 'my_favorites'

