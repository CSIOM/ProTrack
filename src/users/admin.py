#!/usr/bin/env python
#
# (c) 2015 CSIOM, http://www.csiom.com
#
# This file is part of DeeDee project.
#
# DeeDee is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# DeeDee is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DeeDee.  If not, see <http://www.gnu.org/licenses/>.
#
#%% Authors %%
#Jasvir Singh Grewal <js@csiom.com>
#Aseem Mittal <aseemmittal@csiom.com>

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
