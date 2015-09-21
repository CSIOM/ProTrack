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
%% src/notifications/admin.py %%
This file display usage information that admin requires to edit or add 
in database tables, classes in admin interface. 
"""

from django.contrib import admin

from src.notifications.models import NotificationType, Notifications

class NotificationsAdmin(admin.ModelAdmin):
    exclude = ('is_active',)
    list_display = ['id', 'notification_type', 'is_read']
    model = Notifications
    list_per_page = 10


admin.site.register(NotificationType)
admin.site.register(Notifications, NotificationsAdmin)
