# -*- coding: utf-8 -*-

#Django imports
from django import template
from deliverkindle.favorites.models import *
import redis
import json

r     = redis.Redis(host='127.0.0.1')
register = template.Library()

@register.inclusion_tag('favorites/widget.html', takes_context=True)
def favorites_widget(context):
	try:
		user = context['user']
		book_ids = MyFavorites.objects.filter(user_id=user.id).values_list('book_id', flat=True)
		books = r.hmget('calibre_all_books_hash',book_ids[:30])
	 	#entrys = map(json.loads, books)
	 	entrys = []
	 	for book in books:
	 		try:
	 			v = json.loads(book)
	 			entrys.append(v)
	 		except:
	 			print book
	 			continue;
	except:
		user = {}
		entrys = {}
	return {'entrys':entrys,'user':user}
    	
	
