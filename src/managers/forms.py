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
%% src/managers/forms.py %%
This file contains django form classes that can be used for data entry. 
"""

from django import forms
from src.managers.models import ProjectDetails, TeamMembers, StatusOfProject
from django.contrib.auth.models import User

import itertools

class ProjectDetailForm(forms.ModelForm):
    """Form for adding project details."""
    class Meta:
        model = ProjectDetails
        exclude = ['start_date','end_date','is_inactive','manager', 'project_code']

    def __init__(self, *args, **kwargs):
        super(ProjectDetailForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs={'class':'form-control'}
        self.fields['technologies_required'].widget.attrs={'class':'form-control'}
        self.fields['estimated_time'].widget.attrs={'class':'form-control'}
        self.fields['project_summary'].widget.attrs={'class':'form-control'}



class ProjectSelectForm(forms.ModelForm):
    """Form for selecting projects to add team for it."""
    class Meta:
        model = TeamMembers
        exclude = ['user', 'is_active']
    def __init__(self, manager, *args, **kwargs):
        super(ProjectSelectForm, self).__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(
            queryset=ProjectDetails.objects.filter(manager=manager,
                is_inactive=False).order_by('title'))
        self.fields['project'].widget.attrs={'class':'form-control'}


class AddTeamForm(forms.Form):
    """Form for selecting team for the project."""
    select_members = forms.ModelMultipleChoiceField(required=False,
    widget=forms.CheckboxSelectMultiple, queryset= User.objects.all())

class ProjectStatusForm(forms.ModelForm):
    """Form for selecting and changing states of projects."""
    class Meta:
        model = StatusOfProject
        exclude = ['project','remarks']

    def __init__(self, *args, **kwargs):
        super(ProjectStatusForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs={'class':'form-control', 'placeholder':'jass'}

class ProjectTitleForm(forms.Form):
    """Form for changing title of the project."""
    project_title = forms.CharField()
