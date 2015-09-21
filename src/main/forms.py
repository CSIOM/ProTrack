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
%% src/main/forms.py %%
This file contains django form classes that can be used for data entry. 
"""

from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from src.managers.models import ProjectDetails
from src.main.models import ReportComment, Rating
from django.utils.safestring import mark_safe
from django.forms.widgets import RadioSelect
import datetime


class RatingForm(forms.ModelForm):
    """Form for adding rating to reports."""
    class Meta:
      model = Rating
      exclude = ['rater','report','comment',]

class CommentForm(forms.ModelForm):
    """Form for addding comments."""
    class Meta:
      model = ReportComment
      exclude = ['report', 'commenter',]
      widgets = {
          'comment': forms.Textarea(attrs={'rows':4, 'cols':35}),
        }

class LoginForm(forms.Form):
    """Login Form"""
    username = forms.CharField(label="", max_length=20)
    password = forms.CharField(label ="", max_length=20,
                               widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    """SignUp Form"""
    username = forms.CharField(label="username", max_length=20)
    password = forms.CharField(label ="password", max_length=20,
                               widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label ="Confirm password",
                                            max_length=20,
                                            widget=forms.PasswordInput)
    email = forms.EmailField(max_length=50)


class ViewReportForm(forms.Form):
    """Form for viewing reports"""
    VIEW_CHOICES = (('','------'),('1', 'All'),('2', 'Teamwise'),)
    view = forms.ChoiceField(VIEW_CHOICES)
    project = forms.ModelChoiceField(queryset=ProjectDetails.objects.all())

    def __init__(self, manager, *args, **kwargs):
        super(ViewReportForm, self).__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(
            queryset=ProjectDetails.objects.filter(manager=manager))
        self.fields['view'].widget.attrs={'class':'form-control'}
        self.fields['project'].widget.attrs={'class':'form-control'}

class DateSelectForm(forms.Form):
    """Form for selecting date."""
    date=forms.DateField(label="Select Date", required=False)
    name=forms.ModelChoiceField(queryset=User.objects.all(),required=False)

    def __init__(self, super_user_allow, manager_allow, normal_user_allow,
        superuser, *args, **kwargs):
        super(DateSelectForm, self).__init__(*args, **kwargs)
        if super_user_allow == 0 and not superuser:
            super_user_list = User.objects.values_list('id', flat=True).\
                filter(groups__name='super_user')
            if manager_allow == 1:
                self.fields['name'] = forms.ModelChoiceField(
                    queryset=User.objects.exclude(id__in=super_user_list).filter(),
                    required=False)
            else:
                manager_list = User.objects.values_list('id', flat=True).\
                filter(groups__name='managers')
                self.fields['name'] = forms.ModelChoiceField(
                    queryset=User.objects.exclude(id__in=super_user_list).\
                        exclude(id__in=manager_list).filter(),
                    required=False)
        self.fields['date'].widget.attrs={'id':'id_review_date'}
        self.fields['name'].widget.attrs={'class':'form-control'}


class HorizRadioRenderer(RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class DateRangeSelectionForm(forms.Form):
    """Form for selecting date range."""
    report_type = forms.ChoiceField()
    project = forms.ModelChoiceField(queryset=ProjectDetails.objects.all())
    members = forms.ModelChoiceField(queryset=User.objects.all().order_by('username'), required=False)
    start_date = forms.DateField()
    end_date = forms.DateField(initial=datetime.datetime.utcnow())

    def __init__(self, manager, super_user,*args, **kwargs):
        super(DateRangeSelectionForm, self).__init__(*args, **kwargs)
        if super_user == 1:
            self.fields['project'] = forms.ModelChoiceField(
                queryset=ProjectDetails.objects.all().order_by('title'), required=False)
            VIEW_CHOICES = (('1', 'Member/Project Reports'),('2', 'Complete Project Reports'),
                ('3', 'Memberwise'))
        else:
            self.fields['project'] = forms.ModelChoiceField(
                queryset=ProjectDetails.objects.filter(manager=manager).order_by('title'), required=False)
            VIEW_CHOICES = (('1', 'Member/Project Reports'),('2', 'Complete Project Reports'),)
        self.fields['report_type'] = forms.ChoiceField(VIEW_CHOICES,
            widget=forms.RadioSelect(renderer=HorizRadioRenderer))
        self.fields['project'].widget.attrs={'class':'form-control', 'id':'report-project'}
        self.fields['members'].widget.attrs={'id':'members-report','class':'form-control'}
        self.fields['start_date'].widget.attrs={'class':'form-control'}
        self.fields['end_date'].widget.attrs={'class':'form-control'}


class DateRangeForm(forms.Form):
    """Form for selecting date range."""

    start_date = forms.DateField()
    end_date = forms.DateField(initial=datetime.date.today())

    def __init__(self, *args, **kwargs):
        super(DateRangeForm, self).__init__(*args, **kwargs)

        self.fields['start_date'].widget.attrs={'class':'form-control'}
        self.fields['end_date'].widget.attrs={'class':'form-control'}
