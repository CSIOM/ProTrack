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
%% src/users/views.py %%
This file contains basic methodologies like AddReport and Create Profile
update profile.
"""

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import View

from src.users.forms import AddReportForm
from src.users.forms import ReportItemForm, ProfileForm

from src.managers.models import ProjectDetails
from src.managers.models import TeamMembers

from src.users.models import DailyReport, Gender
from src.users.models import DailyReportItem, Profile

from src.main.models import Struggle
from src.main.views import is_manager
from src.main.views import read_unread_notice
from src.main.forms import CommentForm

from src.notifications.models import ReportNotifications, Notifications
from src.notifications.models import NotificationType

from django.contrib.auth.models import User

import datetime

class AddReport(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddReport, self).dispatch(*args, **kwargs)

    def __init__(self):
        pass

    def get(self, request):
        if 'add_report' in request.GET:
            user = request.user
            reportform = AddReportForm(initial={'user':user}, pro=user)
            reportitemform = ReportItemForm()
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            comment_form = CommentForm()
            return render(request,'users/report_add.html',{'reportform':reportform,
                'reportitemform':reportitemform, 'access_var':access_var,
                'form':comment_form, 'notice_status':notice_status})


    def post(self, request):
        pro = request.user
        reportform = AddReportForm(pro, request.POST)
        reportitemform = ReportItemForm(request.POST)
        if reportform.is_valid() and reportitemform.is_valid():
            user = request.user
            project = request.POST['project']
            report_id = DailyReport.objects.values_list('id',flat=True).filter(user=request.user.id).\
                filter(project=project).filter(date=datetime.date.today())
            if report_id:
                reportformdata = DailyReport.objects.get(pk=report_id[0])
            else:
                reportformdata = reportform.save()
            self_rating_list = request.POST.getlist('self_rating')
            duration_list = request.POST.getlist('duration_in_hours')
            work_done_list = request.POST.getlist('work_done')
            struggle_list = request.POST.getlist('struggle')
            tags_list = request.POST.getlist('tags')
            i = 0
            dailyreportobject = DailyReport.objects.get(pk=reportformdata.id)
            dailyreportobj = DailyReport.objects.values('project__project__manager').\
            filter(id=reportformdata.id)[0]
            user_obj = User.objects.get(pk=dailyreportobj['project__project__manager'])
            if user != user_obj:
                notification_type = NotificationType.objects.get(name='Report')
                notifications = Notifications(notification_type=notification_type)
                notifications.save()
                notifications_obj = Notifications.objects.get(id=notifications.id)
                report_notifications = ReportNotifications(report=dailyreportobject,
                    notifier=user_obj, notifications=notifications_obj)
                report_notifications.save()
            for self_rate in self_rating_list:
                reportitemobj = DailyReportItem(daily_report=dailyreportobject,
                    self_rating=self_rate, duration_in_hours=duration_list[i],
                    work_done=work_done_list[i], struggle=struggle_list[i],
                    tags=tags_list[i])
                reportitemobj.save()
                i = i + 1
            if i == len(work_done_list):
                message = "Report Added"
                error=0
            else:
                message = 'Error: Try again later'
                error=1
            return render(request,'users/report_success.html',{'message':message,'error':error})
        else:
            pro = request.user
            reportform = AddReportForm(pro, request.POST)
            reportitemform = ReportItemForm(request.POST)
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            comment_form = CommentForm()
            return render(request,'users/report_add.html',{'reportform':reportform,
                'reportitemform':reportitemform, 'access_var':access_var,
                'form':comment_form, 'notice_status':notice_status})


class UserProfile(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfile, self).dispatch(*args, **kwargs)

    def __init__(self):
        pass

    def get(self, request):
        if 'add_profile' in request.GET:
            return self.add_profile(request)
        elif 'update_profile' in request.GET:
            return self.update_profile(request)
        else:
            return self.profile_view(request)

    def add_profile(self, request):
        profile_form = ProfileForm()
        access_var = is_manager(request)
        notice_status = read_unread_notice(request)
        return render(request,'users/add_profile.html',{'profile_form':profile_form,
            'access_var':access_var, 'notice_status':notice_status})


    def post(self, request):
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            user = request.user
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            gender_id = int(request.POST['gender'])
            skills = request.POST['skills']
            telephone = request.POST['telephone']
            github = request.POST['github']
            bitbucket = request.POST['bitbucket']
            experience = request.POST['experience']
            gender = Gender.objects.get(pk=gender_id)
            profile_obj = Profile.objects.filter(user=user)
            if profile_obj:
                Profile.objects.filter(user=user).update(user=user,
                    first_name=first_name, last_name=last_name,
                    gender=gender, skills=skills, telephone=telephone,
                    github=github, bitbucket=bitbucket, experience=experience)
            else:
                profile = Profile(user=user, first_name=first_name, last_name=last_name,
                    gender=gender, skills=skills, telephone=telephone,
                    github=github, bitbucket=bitbucket, experience=experience)
                profile.save()
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            return render(request,'users/profile_success.html',{'access_var':access_var,
                'notice_status':notice_status})
        else:
            profile_form = ProfileForm(request.POST)
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            return render(request,'users/add_profile.html',{'profile_form':profile_form,
                'access_var':access_var, 'notice_status':notice_status})


    def update_profile(self, request):
        user = request.user
        profile_data = Profile.objects.values('first_name', 'last_name',
            'gender', 'skills', 'telephone', 'github', 'bitbucket',
            'experience').filter(user=user)[0]
        profile_form = ProfileForm(initial={'first_name':profile_data['first_name'],
            'last_name':profile_data['last_name'],'gender':profile_data['gender'],
            'skills':profile_data['skills'], 'telephone':profile_data['telephone'],
            'github':profile_data['github'], 'bitbucket':profile_data['bitbucket'],
            'experience':profile_data['experience']})
        access_var = is_manager(request)
        notice_status = read_unread_notice(request)
        return render(request,'users/add_profile.html',{'profile_form':profile_form,
            'access_var':access_var, 'notice_status':notice_status})


    def profile_view(self, request):
        user = request.user
        profile_info = Profile.objects.filter(user=user)
        if not profile_info:
            return self.add_profile(request)
        profile_info = Profile.objects.filter(user=user)[0]
        access_var = is_manager(request)
        notice_status = read_unread_notice(request)
        return render(request,'users/profile.html',{'profile_info':profile_info,
            'access_var':access_var, 'notice_status':notice_status})
