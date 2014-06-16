# -*- coding: utf-8 -*-
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

from django.contrib import admin
from models import *

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title','author','sub_time','latest_response','click_times')

admin.site.register(Topic,TopicAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)