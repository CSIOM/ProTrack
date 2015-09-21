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
%% src/main/models.py %%
This file contains django model classes that will be used for ORM with database.. 
"""


from django.db import models
from django.contrib.auth.models import User
#from tinymce.models import HTMLField
import datetime
from src.users.models import DailyReport

class ReportComment(models.Model):
    """Model class for comments."""
    comment = models.TextField()
    report = models.ForeignKey(DailyReport)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    commenter = models.ForeignKey(User)

class Rating(models.Model):
    """Model class for Rating"""
    rater = models.ForeignKey(User)
    rating = models.IntegerField()
    report = models.ForeignKey(DailyReport)
    comment = models.ForeignKey(ReportComment)

class Struggle(models.Model):
    """Model class for adding struggle type."""
    struggle_type = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.struggle_type)

class Reviewed(models.Model):
    """Model class for handeling review data."""
    report = models.ForeignKey(DailyReport)
    reviewer = models.ForeignKey(User)
    is_claimed = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)

class TimeTrackingData(models.Model):
    """Model class for holding temporary data required for time tracking"""
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    user = models.ForeignKey(User)
    work_done = models.TextField(null=True)

class UserOfTimer(models.Model):
    """Model to track user of Time Tracker"""
    user = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)

class PauseTimer(models.Model):
    """Model to store pause instances in timer."""
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    currenlty_paused = models.BooleanField(default=True)
    user = models.ForeignKey(User)
