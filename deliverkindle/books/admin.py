# -*- coding: utf-8 -*-


from django.contrib import admin
from models import *


class MultiDBModelAdmin(admin.ModelAdmin):
    # 为方便起见定义一个数据库名称常量。
    using = 'slave'

    def save_model(self, request, obj, form, change):
        # 让 Django 保存对象到 'other' 数据库。
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # 让 Django 从 'other' 数据库中删除对象。
        obj.delete(using=self.using)

    def queryset(self, request):
        # 让 Django 在 'other' 数据库中搜索对象。
        return super(MultiDBModelAdmin, self).queryset(request).using(self.using)

class BooksAdmin(MultiDBModelAdmin):
	list_display = ('id','title', 'timestamp','author_sort')
class CommentsAdmin(MultiDBModelAdmin):
	list_display = ('id','book', 'text')
class SeriesIdClickAdmin(MultiDBModelAdmin):
	list_display = ('id','click')
class UserBookIdAdmin(MultiDBModelAdmin):
	list_display = ('id','userid','bookid')
class BooksplusIdClickAdmin(MultiDBModelAdmin):
	list_display = ('id','click')
class CommentsAdmin(MultiDBModelAdmin):
	list_display = ('id','book', 'text')
class PublishersAdmin(MultiDBModelAdmin):
	list_display = ('id','name')
class DataAdmin(MultiDBModelAdmin):
	list_display = ('id','book', 'format', 'uncompressed_size', 'name')
class BooksSeriesLinkAdmin(MultiDBModelAdmin):
	list_display = ('id','book','series')
class TagsAdmin(MultiDBModelAdmin):
	list_display = ('id','name')
class SeriesAdmin(MultiDBModelAdmin):
    list_display = ('id','name', 'sort')
admin.site.register(Books, BooksAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(SeriesIdClick, SeriesIdClickAdmin)
admin.site.register(UserBookId, UserBookIdAdmin)
admin.site.register(BooksplusIdClick, BooksplusIdClickAdmin)
admin.site.register(Publishers, PublishersAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(BooksSeriesLink, BooksSeriesLinkAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Series, SeriesAdmin)