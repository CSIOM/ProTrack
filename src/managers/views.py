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
%% src/managers/views.py %%
This file contains basic methodologies like Project Details, Project Options 
and Team Members for DeeDee project.
"""

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import View
from django.contrib.auth.models import User
from src.managers.models import ProjectDetails, TeamMembers, Status, StatusOfProject
from src.managers.forms import ProjectDetailForm, AddTeamForm, ProjectSelectForm
from src.managers.forms import ProjectStatusForm, ProjectTitleForm
from src.main.views import is_manager
from src.main.views import read_unread_notice
from src.main.helper import code_generator
from src.notifications.models import Notifications, TeamAddedNotifications
from src.notifications.models import NotificationType
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from src.config import _ADMIN_MAIL as _SENDER_EMAIL
from src.config import _DOMAIN as domain

import datetime

class Project(View):
    """
    Class that handels Project related functionality.
    request: Http Request
    pass: get(self, request)
    """

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.groups.filter(
        name='managers').count() == 1 or u.is_superuser, login_url='/access_denied/'))
    def dispatch(self, *args, **kwargs):
        return super(Project, self).dispatch(*args, **kwargs)

    def list_project(self, request):
        project_list = ProjectDetails.objects.filter(manager=request.user).order_by('-id')
        access_var = is_manager(request)
        notice_status = read_unread_notice(request)
        post_method = 0
        if request.POST:
            post_method = 1
        return render(request,'managers/list_project.html',{'list': project_list,
            'access_var':access_var, 'notice_status':notice_status,
            'method':post_method})

    def add_project(self, request):
        form = ProjectDetailForm()
        access_var = is_manager(request)
        notice_status = read_unread_notice(request)
        return render(request, 'managers/add_project.html',{'form':form,
            'access_var':access_var, 'notice_status':notice_status})

    def post(self, request):
        form = ProjectDetailForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            manager = request.user
            title = formdata['title']
            max_id = ProjectDetails.objects.values_list('id', flat=True).\
                order_by("-id")[0]
            code = code_generator(title, manager.username, max_id)
            tech = formdata['technologies_required']
            time_est = formdata['estimated_time']
            summary = formdata['project_summary']
            data = ProjectDetails(title=title, project_code=code, 
                technologies_required=tech, estimated_time=time_est,
                manager=manager,project_summary=summary)
            data.save()
            team = TeamMembers(project=data, user=request.user)
            team.save()
            return self.list_project(request)
        else:
            form = ProjectDetailForm(request.POST)
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            return render(request, 'managers/add_project.html',{'form':form,
                'access_var':access_var, 'notice_status':notice_status})

    def get(self,request):
        """
        Handels get request and call appropriate function according 
        to arguments in get request.
        Allowed arguments:
        1. add_project: for adding projects and its details
        2. list_project: for listing the project that user added
        """
        try:
            request.GET['add_project']
            return self.add_project(request)
        except:
            return self.list_project(request)

class AddTeam(View):
    """
    Class that handels the functionality of adding the team in the project.
    request: Http Request
    pass: get(self, request)
    """

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.groups.filter(
        name='managers').count() == 1 or u.is_superuser, login_url='/access_denied/'))
    def dispatch(self, *args, **kwargs):
        return super(AddTeam, self).dispatch(*args, **kwargs)

    def post(self, request):
        login_user = request.user
        manager=request.user.id
        project_form = ProjectSelectForm(manager, request.POST)
        if project_form.is_valid() or 'project_id' in request.POST:
            members = request.POST.getlist('select_members')
            try:
                project_id = request.POST['project_id']
                team = TeamMembers.objects.values_list('id',flat=True).\
                    filter(project=project_id).exclude(user = manager)
                current_team = list(TeamMembers.objects.values_list('user__id',flat=True).\
                    filter(project=project_id))
                for val in team:
                    TeamMembers.objects.filter(pk=val).update(is_active=False)
            except:
                project_id = request.POST['project']
                current_team = TeamMembers.objects.values_list('user_id',flat=True).\
                    filter(project=project_id)
            project = ProjectDetails.objects.get(pk=project_id)
            for user_id in members:
                team = TeamMembers.objects.values_list('user__id',flat=True).\
                    filter(project=project).filter(user=user_id)
                if team:
                    TeamMembers.objects.filter(project=project).filter(user=user_id).\
                    update(is_active=True)
                else:
                    user = User.objects.get(pk=user_id)
                    TeamMembers(user=user, project=project).save()
                    if user != login_user:
                        in_previous_team = False
                        for current_team_member in current_team:
                            if int(user_id) == int(current_team_member):
                                in_previous_team = True
                                break
                        if in_previous_team:
                            pass
                        else:
                            notification_type = NotificationType.objects.get(name='Team Added')
                            notifications = Notifications(notification_type=notification_type)
                            notifications.save()
                            notifications_obj = Notifications.objects.get(id=notifications.id)
                            TeamAddedNotifications(project_details=project,
                                notifier=user, notifications=notifications_obj).save()
                            temp = Context({'user':user.username,'title':project.title,
                                'manager':project.manager,'summary':project.project_summary,
                                'domain':domain,'project_id':project.id})
                            plaintext = get_template('managers/team_added_mail.txt')
                            content = get_template('managers/team_added_mail.html')
                            html_content = content.render(temp)
                            subject, from_email, to = 'You are in Team', _SENDER_EMAIL, user.email
                            text_content = plaintext.render(temp)
                            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                            msg.attach_alternative(html_content, "text/html")
                            msg.send()
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            return render(request,'managers/team_added.html',{'access_var':access_var,
                'notice_status':notice_status})
        else:
            team_list = []
            team_id = User.objects.values_list('id', flat=True).order_by('username')
            for val in team_id:
                temp = {}
                temp['id'] = val
                username = User.objects.values_list('username',flat=True).filter(id=val)[0]
                temp['username'] = username
                active_projects = TeamMembers.objects.values_list('id',flat=True).\
                    filter(user=val).filter(project__is_inactive=False, is_active=True)
                project_count = len(active_projects)
                temp['project_count'] = project_count
                team_list.append(temp)
            project_form = ProjectSelectForm(manager, request.POST)
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            return render(request,'managers/add_team.html',{'team_list':team_list,
                'project_form':project_form, 'access_var':access_var, 
                'notice_status':notice_status})


    def get(self, request):
        team_list = []
        team_id = User.objects.values_list('id', flat=True).filter(is_staff=True).order_by('username')
        if 'edit_id' in request.GET:
            current_team = TeamMembers.objects.values_list('user',flat=True).\
                filter(project=request.GET['edit_id'], is_active=True)
        else:
            current_team = []
        for val in team_id:
            temp = {}
            temp['id'] = val
            username = User.objects.values_list('username',flat=True).filter(id=val)[0]
            temp['username'] = username
            active_projects = TeamMembers.objects.values_list('id',flat=True).\
                filter(user=val).filter(project__is_inactive=False, is_active=True)
            project_count = len(active_projects)
            temp['project_count'] = project_count
            if val in current_team:
                temp['selected'] = 'checked'
            team_list.append(temp)
        if 'edit_id' in request.GET:
            project = ProjectDetails.objects.get(pk=request.GET['edit_id'])
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            return render(request,'managers/add_team.html',{'team_list':team_list,
                'project':project, 'access_var':access_var, 
                'notice_status':notice_status})
        else:
            project_form = ProjectSelectForm(manager=request.user)
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            return render(request,'managers/add_team.html',{'team_list':team_list,
                'project_form':project_form, 'access_var':access_var, 
                'notice_status':notice_status})

class ProjectOptions(View):
    """
    Class that handels project related functionality like mark as started or
    finished.
    request: Http Request
    pass: get(self, request)
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProjectOptions, self).dispatch(*args, **kwargs)

    def mark_as_finished(self,request):
        project_id = request.GET['project']
        now = datetime.date.today()
        ProjectDetails.objects.filter(id=project_id).update(end_date=now, 
            is_inactive=True)
        project = ProjectDetails.objects.get(pk=project_id)
        start_date=0
        end_date=0
        if project.start_date:
            start_date = 1
        if project.end_date:
            end_date = 1
        access_var = is_manager(request)
        notice_status = read_unread_notice(request)
        return render(request,'managers/project_details.html',
            {'project':project,'start': start_date, 'end':end_date,
            'access_var':access_var, 'notice_status':notice_status})

    def mark_as_started(self,request):
        project_id = request.GET['project']
        now = datetime.date.today()
        ProjectDetails.objects.filter(id=project_id).update(start_date=now)
        project = ProjectDetails.objects.get(pk=project_id)
        start_date=''
        end_date=''
        if project.start_date:
            start_date = 1
        if project.end_date:
            end_date = 1
        access_var = is_manager(request)
        notice_status = read_unread_notice(request)
        return render(request,'managers/project_details.html',
            {'project':project,'start': start_date, 'end':end_date,
            'access_var':access_var, 'notice_status':notice_status})

    def get(self, request):
        """
        Handels get request and call appropriate function according 
        to arguments in get request.
        Allowed arguments:
        1. mark_as_started: for starting the project
        2. mark_as_finished: for finishing the project
        """
        self.user = request.user
        try:
            request.GET['mark_as_finished']
            return self.mark_as_finished(request)

        except:
            try:
                request.GET['mark_as_started']
                return self.mark_as_started(request)

            except:
                project_id = request.GET['project']
                project = ProjectDetails.objects.get(pk=project_id)
                try:
                    status = StatusOfProject.objects.values_list('status__state',
                        flat=True).filter(project=project_id).order_by('-id')[0]
                except:
                    status = 'Not started yet'

                if 'review' in request.GET:
                    notice = request.GET['notice']
                    Notifications.objects.filter(id=notice).update(is_read=True)
                start_date=0
                end_date=0
                if project.start_date:
                    start_date = 1
                if project.end_date:
                    end_date = 1
                access_var = is_manager_of_project(self.user.id,project_id)
                team_list = TeamMembers.objects.values_list('user__username',flat=True).\
                    filter(project=project_id, is_active=True)
                notice_status = read_unread_notice(request)
                team_size = len(team_list)
                return render(request,'managers/project_details.html',
                    {'project':project,'start': start_date, 'end':end_date,
                    'access_var':access_var, 'notice_status':notice_status,
                    'team_list':team_list,'team_size':team_size,'status':status})


def is_manager_of_project(user_id,project_id):
    manager_id = ProjectDetails.objects.get(pk=project_id)
    if manager_id.manager.id == user_id:
        user_allow = 1
    else:
        user_allow = 0

    return user_allow

def access_denied(request):
    """
    Function that handels the error display for user where not allowed to visit.
    request: Http Request
    pass: render access_denied.html
    """
    access_var = is_manager(request)
    notice_status = read_unread_notice(request)
    return render(request, 'access_denied.html',{'access_var':access_var,
        'notice_status':notice_status})

@login_required
def change_status(request):
    project = request.GET['project']
    try:
        status = request.GET['status']
        remarks = request.GET['remarks']
        project_obj = ProjectDetails.objects.get(pk=project)
        status_obj = Status.objects.get(pk=status)
        if status_obj.make_active_tag:
            if project_obj.start_date:
                ProjectDetails.objects.filter(id=project).\
                update(is_inactive=False)

            else:
                ProjectDetails.objects.filter(id=project).\
                update(is_inactive=False,start_date=datetime.\
                    datetime.today())


        if status_obj.make_inactive_tag:
            ProjectDetails.objects.filter(id=project).\
            update(is_inactive=True,end_date=datetime.\
                datetime.today())
        StatusOfProject(project=project_obj, status=status_obj,
            remarks=remarks).save()
        return HttpResponse(status_obj.state)

    except:
        try:
            status_id = StatusOfProject.objects.values_list('id',flat=True).\
            filter(project=project).order_by('-id')[0]
            status_obj = StatusOfProject.objects.get(pk=status_id)
            form = ProjectStatusForm(instance=status_obj)
        except:
            form = ProjectStatusForm()
        temp = Context({'form':form, 'project':project})
        content = get_template('managers/change_status.html')
        html_content = content.render(temp)
        return HttpResponse(html_content)

@login_required
def view_history(request):
    project = request.GET['project']
    project_status_list = StatusOfProject.objects.values('status__state',
        'datetime', 'remarks').filter(project=project).order_by('-id')
    temp = Context({'project_status_list':project_status_list})
    content = get_template('managers/history.html')
    html_content = content.render(temp)
    return HttpResponse(html_content)

@login_required
def change_project_title(request):
    project = request.GET['project']
    try:
        project_title = request.GET['project_title']
        ProjectDetails.objects.filter(id=project).update(title=project_title)
        return HttpResponse('')

    except:
        project_title = ProjectDetails.objects.values_list('title',flat=True).\
        filter(id=project)[0]
        form = ProjectTitleForm(initial={'project_title':project_title})
        temp = Context({'form':form, 'project':project})
        content = get_template('managers/change_project_title.html')
        html_content = content.render(temp)
        return HttpResponse(html_content)