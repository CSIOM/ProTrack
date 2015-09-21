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
