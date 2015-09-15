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
%% src/notifications/models.py %%
This file contains django model classes that will be used for ORM with database.. 
"""

from django.db import models

from django.contrib.auth.models import User

from src.users.models import DailyReport

from src.main.models import ReportComment

from src.managers.models import ProjectDetails


class NotificationType(models.Model):
    """Model class for Notification Type."""
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return unicode(self.name)


class Notifications(models.Model):
    """Model class for read-unread notification type."""
    notification_type = models.ForeignKey(NotificationType)
    date_time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class ReportNotifications(models.Model):
    """Model class for Reports Notifications."""
    report = models.ForeignKey(DailyReport)
    notifier = models.ForeignKey(User)
    notifications = models.ForeignKey(Notifications)


class CommentNotifications(models.Model):
    """Model class for Comment Notifications."""
    report = models.ForeignKey(DailyReport)
    comment = models.ForeignKey(ReportComment)
    notifier = models.ForeignKey(User)
    notifications = models.ForeignKey(Notifications)


class TeamAddedNotifications(models.Model):
    """Model class for TeamAdded Notifications."""
    project_details = models.ForeignKey(ProjectDetails)
    notifier = models.ForeignKey(User)
    notifications = models.ForeignKey(Notifications)