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
%% src/mamagers/models.py %%
This file contains django model classes that will be used for ORM with database.. 
"""

from django.db import models
from django.contrib.auth.models import User

class ProjectDetails(models.Model):
    """Model class for project."""
    title = models.CharField(max_length=100, verbose_name="Project Title")
    project_code = models.CharField(max_length=20, blank=True, null=True)
    technologies_required = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    estimated_time = models.CharField(max_length=10)
    is_inactive = models.BooleanField(default=False)
    manager = models.ForeignKey(User)
    project_summary = models.TextField()

    class Meta:
        verbose_name_plural="Project Details"

    def __unicode__(self):
        return self.title

class TeamMembers(models.Model):
    """Model class for team members of the project."""
    project = models.ForeignKey(ProjectDetails)
    user = models.ForeignKey(User)
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "Team Members"

    def __unicode__(self):
        return unicode(self.project)

class Status(models.Model):
    """Model class for listing states of projects."""
    state = models.CharField(max_length=200,help_text="Name of status field")
    make_active_tag = models.BooleanField(default=False,
        help_text="Mark me if this state makes project active(started/resumed etc)")
    make_inactive_tag = models.BooleanField(default=False,
        help_text="Mark me if this state makes project inactive(completed/cancelled etc)")

    class Meta:
        verbose_name_plural = "Status"

    def __unicode__(self):
        return self.state

class StatusOfProject(models.Model):
    """Model class to store status of projects."""
    project = models.ForeignKey(ProjectDetails)
    status = models.ForeignKey(Status)
    remarks = models.TextField(default=None)
    datetime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.project
