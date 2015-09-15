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
%% src/users/forms.py %%
This file contains django form classes that can be used for data entry. 
"""

from django import forms

from src.users.models import DailyReport
from src.users.models import DailyReportItem, Profile

from src.managers.models import TeamMembers

class AddReportForm(forms.ModelForm):
    """Form class for adding report of the day."""

    class Meta:
        model = DailyReport
        widgets = {'user': forms.HiddenInput()}

    def __init__(self, pro, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(AddReportForm, self).__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(queryset=TeamMembers.objects.\
            filter(user=pro, project__is_inactive=False, is_active=True))
        self.fields['project'].widget.attrs={'class':'form-control'}


class ReportItemForm(forms.ModelForm):
    """Form class for adding ReportItem for a report as ther can be multiple
    work done by single person. He/she can add as many form entity required."""

    class Meta:
        model = DailyReportItem
        exclude = ('daily_report',)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ReportItemForm, self).__init__(*args, **kwargs)
        self.fields['self_rating'].widget.attrs={'class': 'self_rating_class form-control'}
        self.fields['duration_in_hours'].widget.attrs={'class': 'class_duration_in_hours form-control'}
        self.fields['work_done'].widget.attrs={'class':'form-control', 'cols':20, 'rows':1}
        self.fields['struggle'].widget.attrs={'class':'form-control', 'cols':20, 'rows':1}
        self.fields['tags'].widget.attrs={'class':'form-control', 'cols':20, 'rows':1}


class ProfileForm(forms.ModelForm):
    """Form class for profile."""

    class Meta:
        model = Profile
        exclude = ['user']
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs={'class':'form-control'}
        self.fields['last_name'].widget.attrs={'class':'form-control'}
        self.fields['gender'].widget.attrs={'class':'form-control'}
        self.fields['skills'].widget.attrs={'class':'form-control'}
        self.fields['telephone'].widget.attrs={'class':'form-control'}
        self.fields['github'].widget.attrs={'class':'form-control'}
        self.fields['bitbucket'].widget.attrs={'class':'form-control'}
        self.fields['experience'].widget.attrs={'class':'form-control'}