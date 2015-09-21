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
%% src/notifications/views.py %%
This file contains methodologies for notifications display for DeeDee project.
"""

from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from src.notifications.models import ReportNotifications, CommentNotifications
from src.notifications.models import Notifications
from src.main.views import is_manager
from src.main.views import read_unread_notice

class Notification(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Notification, self).dispatch(*args, **kwargs)

    def __init__(self):
        pass

    def get(self, request):
        return self.notification_list(request)


    def notification_list(self, request):
        user = request.user
        val_list = Notifications.objects.filter(Q(reportnotifications__notifier=user) |
            Q(commentnotifications__notifier=user) |
            Q(teamaddednotifications__notifier=user)).values('is_read', 'id',
            'reportnotifications__report__user__username',
            'commentnotifications__report__user__username',
            'reportnotifications__report', 'commentnotifications__report',
            'reportnotifications__report__date',
            'reportnotifications__report__time',
            'commentnotifications__comment__date',
            'commentnotifications__comment__time',
            'notification_type__name', 'commentnotifications__report__date',
            'reportnotifications__report__project__project__title',
            'commentnotifications__report__project__project__title',
            'reportnotifications__id', 'commentnotifications__id',
            'commentnotifications__comment__commenter__username',
            'commentnotifications__report__time',
            'teamaddednotifications__project_details__manager__username',
            'teamaddednotifications__project_details__title',
            'teamaddednotifications__project_details__id',
            'teamaddednotifications__id', 'date_time'
            ).order_by('-date_time')
        access_var = is_manager(request)
        notice_status = read_unread_notice(request)
        return render(request, 'notifications/notifications.html', {
            'val_list':val_list, 'access_var':access_var,
            'notice_status':notice_status})
