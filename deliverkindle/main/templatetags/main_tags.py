#encoding:utf-8

# -*- coding: utf-8 -*-

from django.contrib.comments.models import Comment
from django.template import Library

register = Library()

@register.inclusion_tag('latest_comment.tag.html')
def get_latest_comment(count=6):
    comments = Comment.objects.order_by('-id')[0:count]
    return {'comments':comments}

