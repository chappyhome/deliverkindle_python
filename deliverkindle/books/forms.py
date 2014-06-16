#encoding:utf-8

from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(label='',required=False,max_length=50,min_length=1)