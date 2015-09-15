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
%% src/managers/admin.py %%
This file display usage information that admin requires to edit or add 
in database tables, classes in admin interface. 
"""

from django.contrib import admin
from src.managers.models import *

class ProjectDetailsAdmin(admin.ModelAdmin):
	model = ProjectDetails
	list_display = ['title','project_code','estimated_time','manager']
	list_filter = ['is_inactive','manager']
	list_per_page = 20 

class TeamMembersAdmin(admin.ModelAdmin):
	model = TeamMembers
	list_display = ['project','user']
	list_per_page = 20 

admin.site.register(ProjectDetails, ProjectDetailsAdmin)
admin.site.register(TeamMembers, TeamMembersAdmin)
admin.site.register(Status)