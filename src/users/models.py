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
%% src/users/models.py %%
This file contains django model classes that will be used for ORM with database.
"""


from django.db import models
from django.contrib.auth.models import User

from src.managers.models import ProjectDetails
from src.managers.models import TeamMembers

import datetime

class DailyReport(models.Model):
    """Model class for adding report"""
    user = models.ForeignKey(User)
    project = models.ForeignKey(TeamMembers)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s' % (self.user) + ' on ' '%s' % (self.date)


class DailyReportItem(models.Model):
    """Models class for adding report item."""
    daily_report = models.ForeignKey(DailyReport)
    self_rating = models.IntegerField(default=100)
    duration_in_hours = models.CharField(max_length=5)
    work_done = models.TextField()
    struggle = models.TextField(default='Null')
    tags = models.TextField(blank=True)


class Gender(models.Model):
    """Model class for gender to use as foreign key in profile."""
    gender_type = models.CharField(max_length=100)
    def __unicode__(self):
        return '%s' % (self.gender_type)


class Profile(models.Model):
    """Model class for adding profile."""
    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    gender = models.ForeignKey(Gender)
    skills = models.TextField(max_length=500)
    telephone = models.CharField(max_length=500)
    github = models.CharField(max_length=500)
    bitbucket = models.CharField(max_length=500)
    experience = models.TextField(max_length=500)
