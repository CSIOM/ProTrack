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
%% src/main/admin.py %%
This file display usage information that admin requires to edit or add 
in database tables, classes in admin interface. 
"""

from django.contrib import admin
from src.main.models import *
from django.contrib.admin.models import LogEntry


admin.site.register(Struggle)
admin.site.register(ReportComment)
admin.site.register(Rating)
admin.site.register(Reviewed)

class UserOfTimerAdmin(admin.ModelAdmin):
	model = UserOfTimer
	list_display = ['user', 'datetime']
	list_filter = ['datetime']
	list_per_page = 20

class LogEntryAdmin(admin.ModelAdmin):
    """
    This class is used to see logs in a detailed format. It is far much
    better than django recent actions widget.
    """
    model = LogEntry
    list_display = ['id','user','object_repr','content_type','action_time']
    list_filter = ['action_time']
    search_fields = ['object_repr']
    list_per_page = 20

admin.site.register(UserOfTimer, UserOfTimerAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
