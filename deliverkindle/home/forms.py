#encoding:utf-8
"""
pythoner.net
Copyright (C) 2013  PYTHONER.ORG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from django import forms
from deliverkindle.accounts.models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        widgets = {'introduction':forms.Textarea()}
        exclude = ('score','deleted','photo','user','city')

class PhotoForm(forms.Form):
    photo = forms.ImageField(label='',max_length=1024)