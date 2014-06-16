import sys, os.path 
sys.path.append("/home/data/www.deliverkindle.com")
#export DJANGO_SETTINGS_MODULE=deliverkindle.settings
from deliverkindle.settings import *
from deliverkindle.books.models import Series, BooksAdd
from deliverkindle.favorites.models import MyFavorites
from django.core.management import *
from django.db import connections

#import MySQLdb
DataName = 'slave'
cursor = connections[DataName].cursor()
cursor.execute('drop view if exists booksplus')
sql = 'create view if not exists booksplus as select books.id,data.name,group_concat(data.format),data.uncompressed_size,title,timestamp,pubdate, isbn ,path,uuid, has_cover, text as descript,\
		      author_sort as author from (books left join data on books.id = data.book) left join comments on books.id = comments.book group by uuid'
cursor.execute(sql)
