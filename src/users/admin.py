#!/usr/bin/env python
"""
This file is part of piPi project.

Copyright (C) 2015 CSIOM, http://www.csiom.com
Authors: The Csiom Team

piPi is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

"""

"""
%% src/users/admin.py %%
This file display usage information that admin requires to edit or add 
in database tables, classes in admin interface. 
"""

from django.contrib import admin
from src.users.models import *

class DailyReportAdmin(admin.ModelAdmin):
	list_display = ['user','project','date','time']
	list_filter = ['user']
	list_per_page = 20

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user','first_name','last_name']
	list_filter = ['user']
	list_per_page = 20

class DailyReportItemAdmin(admin.ModelAdmin):
	list_display = ['daily_report','self_rating','duration_in_hours','work_done']

admin.site.register(DailyReport,DailyReportAdmin)
admin.site.register(DailyReportItem, DailyReportItemAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Gender)
