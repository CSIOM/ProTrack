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
%% src/main/views.py %%
This file contains basic methodologies like SignUp, Index page etc 
for DeeDee project. It also include methodologies for implementing 
reverse in JavaScript and checking group of request user.
"""


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from src.main.forms import RegisterForm, LoginForm, ViewReportForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.contrib.auth import update_session_auth_hash
from src.users.models import DailyReport
from django.template import Context
from django.template.loader import get_template
from src.managers.models import ProjectDetails, TeamMembers
from src.users.models import DailyReportItem, Profile
from src.users.forms import AddReportForm, ReportItemForm
from src.main.forms import CommentForm, RatingForm, DateSelectForm, DateRangeSelectionForm
from src.main.forms import DateRangeForm
from src.main.models import ReportComment, Rating, Reviewed
from src.main.models import TimeTrackingData, UserOfTimer, PauseTimer
from src.notifications.models import ReportNotifications, NotificationType
from src.notifications.models import CommentNotifications, Notifications
import simplejson
import datetime
import pytz
from collections import OrderedDict

class MainIndex(View):
    """Class Handeling Index requests.
    request: Http Request
    pass: get(self,request)
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MainIndex, self).dispatch(*args, **kwargs)

    def __init__(self):
        pass

    def get(self, request):
        """
        Returns: Add profile page if user don't have an active profile.
        Else redirect to Index page.
        """
        user = request.user
        projects = ProjectDetails.objects.filter(teammembers__user=user.id, 
            is_inactive=False)
        access_var = is_manager(request)
        notice_status = read_unread_notice(request)
        profile = Profile.objects.filter(user=request.user.id)
        if profile:
            return render(request,'index.html',{'user':user, 'project':projects,
            'access_var':access_var, 'notice_status':notice_status})
        else:
            """If user don't have an active profile, he/she will 
            automatically get redirected to profile page."""
            return HttpResponseRedirect(reverse('user_profile'))


class SignUp(View):
    """Class that handels SignUp requests.
    request: Http Request.
    pass: get(self, request), if get request. Else post(self,request).
    """
    form_class = RegisterForm
    template_name  = 'registration/registration_form.html'


    def get(self, request, *args, **kwargs):
        """Returns SignUp form."""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        """Handels post request for SignUp class and create user id."""
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'].lower(),
                    form.cleaned_data['email'],
                    form.cleaned_data['password'])
            user.save()

            return render(self.request, "registration/registration_complete.html")

class ViewReport(View):
    """Class that handels ViewReport functionality.
    request: Http Request
    pass: get(self, request)
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ViewReport, self).dispatch(*args, **kwargs)

    def get(self, request):
        """Handels get request and call appropriate function according 
        to arguments in get request.
        Allowed arguments:
        1. list_report: for listing reports of request.user
        2. view_val: Handels Ajax Request for listing reports according
        to users or projects.
        3. report_info: For viewing a particular report.
        """
        if 'list_report' in request.GET:
            return self.list_report(request)
        elif 'view_val' in request.GET:
            return self.result_report(request)
        elif 'report_info' in request.GET or 'report_summary' in request.GET:
            return self.report_info(request)
        else:
            access_var = is_manager(request)
            if access_var == 1:
                manager = request.user
                form = ViewReportForm(manager=manager)
                notice_status = read_unread_notice(request)
                return render(request,'main/view_report_options.html',{'form':form,
                    'access_var':access_var, 'notice_status':notice_status})
            else:
                return self.list_report(request)

    def result_report(self, request):
        view_val = int(request.GET['view_val'])
        if view_val == 1:
            manager_id = request.user.id
            var_list = TeamMembers.objects.values('user__id', 'user__username',
                'project').filter(project__manager=manager_id)
            temp = Context({'var_list':var_list, 'view_val':view_val})
            content = get_template('main/report_search_result.html')
            html_content = content.render(temp)
            return HttpResponse(html_content)
        elif view_val == 2:
            project_val = request.GET['project_val']
            user_id = request.user
            user_list = TeamMembers.objects.values_list('user_id', flat=True).\
            filter(project=project_val)
            var_list = User.objects.values('id', 'username').filter(
                id__in=user_list)
            temp = Context({'var_list':var_list, 'project_id':project_val})
            content = get_template('main/report_search_result.html')
            html_content = content.render(temp)
            return HttpResponse(html_content)

    def list_report(self, request):
        if 'user_id' in request.GET:
            user_id = int(request.GET['user_id'])
            project_id = request.GET['project_id']
            access_var = is_manager(request)
            login_user = request.user.id
            manager_list = User.objects.values_list('id', flat=True).filter(
                groups__name='managers')
            if user_id == login_user or login_user in manager_list:
                daily_report = DailyReport.objects.filter(user=user_id,
                    project__project=project_id).order_by('-date', '-time')
                report_list = []
                for value in daily_report:
                    temp = []
                    temp.append(value.id)
                    temp.append(value.project)
                    temp.append(value.date)
                    temp.append(value.time)
                    temp.append(value.user_id)
                    daily_report_item = DailyReportItem.objects.values_list('duration_in_hours',
                        flat=True).filter(daily_report=value.id)
                    total_hours = hours(*daily_report_item)
                    total_minutes = minutes(*daily_report_item)
                    total_duration = str(total_hours).zfill(2) + ':' + str(total_minutes).zfill(2)
                    temp.append(total_duration)
                    report_list.append(temp)
                access_var = is_manager(request)
                try:
                    return render(request,'main/list_report.html',{'list': report_list,
                        'access_var':access_var, 'notice_status':notice_status})
                except:
                    return render(request,'main/list_report.html',{'list': report_list,
                        'access_var':access_var})
            else:
                access_var = is_manager(request)
                notice_status = read_unread_notice(request)
                return render(request, 'access_denied.html',{'access_var':access_var,
                    'notice_status':notice_status})
        else:
            if 'start_date' in request.GET and 'end_date' in request.GET:
                start_date = request.GET['start_date']
                end_date = request.GET['end_date']
                login_user = request.user
                daily_report = DailyReport.objects.filter(user=login_user,
                    date__range=(start_date,end_date)).order_by('-date', '-time')
                report_list = []
                for value in daily_report:
                    temp = []
                    temp.append(value.id)
                    temp.append(value.project)
                    temp.append(value.date)
                    temp.append(value.time)
                    temp.append(value.user_id)
                    daily_report_item = DailyReportItem.objects.values_list('duration_in_hours',
                        flat=True).filter(daily_report=value.id)
                    total_hours = hours(*daily_report_item)
                    total_minutes = minutes(*daily_report_item)
                    total_duration = str(total_hours).zfill(2) + ':' + str(total_minutes).zfill(2)
                    temp.append(total_duration)
                    report_list.append(temp)
                duration_list = DailyReportItem.objects.filter(
                    daily_report__date__range=(start_date,end_date),
                    daily_report__user=login_user).values_list(
                    'duration_in_hours', flat=True)
                total_hours = hours(*duration_list)
                total_minutes = minutes(*duration_list)
                temp = Context({'list': report_list, 'total_hours':total_hours,
                    'total_minutes':total_minutes})
                content = get_template('main/list_report.html')
                html_content = content.render(temp)
                return HttpResponse(html_content)
            else:
                form = DateRangeForm()
                return render(request,'main/list_report_form.html',{'form':form})


    def report_info(self, request):
        report_id = request.GET['report_id']
        user_id = DailyReport.objects.values_list('user',flat=True).\
            filter(id=report_id)[0]
        login_user = request.user.id
        daily_report_temp = DailyReport.objects.values_list(
            'project__project__manager', flat=True).filter(id=report_id)
        if 'review' in request.GET:
            notice_id = int(request.GET['notice_id'])
            if 'report' in request.GET:
                Notifications.objects.filter(id=notice_id).update(
                    is_read=True)
            elif 'comment' in request.GET:
                Notifications.objects.filter(id=notice_id).update(
                    is_read=True)
        try:
            reviewer = Reviewed.objects.values_list('reviewer',flat=True).\
                filter(report=report_id)[0]
        except:
            reviewer = ''
        if user_id == login_user or login_user in daily_report_temp or reviewer == login_user\
        or 'report_summary' in request.GET:
            item_list = DailyReportItem.objects.filter(daily_report=report_id)
            written_by_info = DailyReport.objects.values('user__username',
                'project__project__title', 'date', 'user').filter(pk=report_id)[0]
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            rating = Rating.objects.values('rating').filter(rater=login_user).\
                filter(report=report_id)
            if rating or user_id == login_user:
                rate_form_status = ''
            else:
                rate_form_status = 'enabled'
            rate_form = RatingForm()
            comment_form = CommentForm()
            comments = ReportComment.objects.values('commenter__username','comment',
                'date','time', 'rating__rating').filter(report=report_id).order_by('id')
            if 'report_summary' in request.GET:
                temp = Context({'list': item_list, 'report':report_id,
                    'written_by_info':written_by_info, 'login_user':login_user})
                content = get_template('main/report_summary.html')
                html_content = content.render(temp)
                return HttpResponse(html_content)
            else:
                return render(request,'main/report_items.html',{'list': item_list,
                    'access_var':access_var,'form':comment_form,
                    'rate_form':rate_form,'rate_form_status': rate_form_status,
                    'report':report_id,'comments':comments, 'notice_status':notice_status,
                    'written_by_info':written_by_info, 'login_user':login_user})
        else:
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            return render(request, 'access_denied.html',{'access_var':access_var,
                'notice_status':notice_status})


class Comment(View):
    """Class that handels Comments request
    request: Ajax Http Request
    pass: post(self, request)

    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Comment, self).dispatch(*args, **kwargs)

    def add_comment(self,request):
        #report = request.GET['report']
        return HttpResponse('add_comment')

    def post(self, request):
        """
        saves posted comment and rating with user id and report id.
        """
        poster = request.user
        rate_form = RatingForm(request.POST)
        comment_form = CommentForm(request.POST)
        report = request.POST['report_id']
        report_obj = DailyReport.objects.get(pk=report)
        report_object = DailyReport.objects.values('user',
            'project__project__manager').get(pk=report)
        try:
            reviewer = Reviewed.objects.values('reviewer').filter(report=report)[0]
            reviewer_obj = User.objects.get(pk=reviewer['reviewer'])
        except:
            reviewer_obj = ''
        user_obj = User.objects.get(pk=report_object['user'])
        manager_obj = User.objects.get(pk=report_object['project__project__manager'])

        if comment_form.is_valid():
            formdata = comment_form.cleaned_data
            comment = formdata['comment']
            data_comment = ReportComment(comment=comment, commenter=poster, 
                report=report_obj)
            data_comment.save()
            report_comment = ReportComment.objects.get(pk=data_comment.id)
            notification_type = NotificationType.objects.get(name='Comment')
            notifications = Notifications(notification_type=notification_type)
            notifications.save()
            notifications_obj = Notifications.objects.get(id=notifications.id)
            if poster != user_obj:
                comment_notifications = CommentNotifications(report=report_obj,
                    notifier=user_obj, notifications=notifications_obj,
                    comment=report_comment)
                comment_notifications.save()
            if poster != manager_obj:
                comment_notifications = CommentNotifications(report=report_obj,
                    notifier=manager_obj, notifications=notifications_obj,
                    comment=report_comment)
                comment_notifications.save()
            if poster != reviewer_obj and reviewer_obj != '':
                comment_notifications = CommentNotifications(report=report_obj,
                    notifier=reviewer_obj, notifications=notifications_obj,
                    comment=report_comment)
                comment_notifications.save()

        if rate_form.is_valid():
            formdata = rate_form.cleaned_data
            rating = formdata['rating']
            data = Rating(rating=rating,report=report_obj,rater=poster,
                comment=data_comment)
            data.save()

        return HttpResponse('')


    def get(self,request):
        try:
            request.GET['add']
            return self.add_comment(request)
        except:
            return HttpResponse('except')


@login_required
def is_manager(request):
    """
    arguments: Http Request Object
    returns: 1 if request.user is manager else return 0."""
    user = request.user
    is_manager = user.groups.filter(name='managers').exists()
    if is_manager or user.is_superuser:
        user_allow = 1
    else:
        user_allow = 0
    return user_allow


@login_required
def is_super_user(request):
    """
    arguments: Http Request Object
    returns: 1 if request.user is manager else return 0."""
    user = request.user
    super_user = user.groups.filter(name='super_user').exists()
    if super_user or user.is_superuser:
        super_user_allow = 1
    else:
        super_user_allow = 0
    return super_user_allow


@login_required
def is_normal_user(request):
    """
    arguments: Http Request Object
    returns: 1 if request.user is normal user else return 0."""
    user = request.user
    normal_user = user.groups.filter(name='normal_user').exists()
    if normal_user:
        normal_user_allow = 1
    else:
        normal_user_allow = 0
    return normal_user_allow


@login_required
def read_unread_notice(request):
    """
    arguments: Http Request.
    retruns: 1 if there is any unread notification else return 0.
    """
    user = request.user
    obj = Notifications.objects.filter(Q(reportnotifications__notifier=user) | 
        Q(commentnotifications__notifier=user) |
        Q(teamaddednotifications__notifier=user)).filter(is_read=0)
    if obj:
        notice_status = 1
    else:
        notice_status = 0
    return notice_status


@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    password_change_form=PasswordChangeForm):
    #need attention.  May be re-write.
    access_var = is_manager(request)
    notice_status = read_unread_notice(request)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(request,'registration/password_change_done.html',{
                'access_var':access_var, 'notice_status':notice_status})
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': 'Password change',
        'access_var': access_var,
        'notice_status':notice_status
        }
    return TemplateResponse(request, template_name, context)

def jsreverse(request):
    """
    This function reverse looks up the urls for the AJAX Requests
    Argument: Http Request
    Return: Dunamic Url
    """
    string_to_reverse = request.GET['string'];
    return HttpResponse(reverse(string_to_reverse))

class Review(View):
    """
    Class for handeling review functionality.
    request: Http Request
    pass: get(self, request)
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Review, self).dispatch(*args, **kwargs)        

    def get(self, request):
        """
        Handels get request for Rview class.
        """
        access_var = is_manager(request)
        notice_status = read_unread_notice(request)
        super_user_allow = is_super_user(request)
        manager_allow = is_manager(request)
        normal_user_allow = is_normal_user(request)
        self.user = request.user
        if 'claim' in request.GET:
            claim = request.GET['claim']
            report = DailyReport.objects.get(pk=claim)
            marked_as_calimed = Reviewed.objects.filter(report=report)
            if marked_as_calimed:
                pass
            else:
                reviewed = Reviewed(report=report,reviewer=request.user,
                    is_claimed=True)
                reviewed.save()

            url = reverse('view_report')
            return HttpResponseRedirect(url + "?report_id=%s" % (claim) + \
                "&user_id=%s" % (self.user.id) + "&report_info")
        elif 'date' in request.GET:
            """If request have date then it return list, else it return
            form only."""
            selected_date = request.GET['date']
            reviewed = Reviewed.objects.values_list('id').filter(is_reviewed=True)
            if 'name' in request.GET:
                name = request.GET['name']
                manager_list = ProjectDetails.objects.values_list('manager', flat=True).filter()
                open_for_review = DailyReport.objects.values('id','user','user__username',
                    'project__project__title','project__project__manager','date','reviewed',
                    'reviewed__is_claimed', 'reviewed__reviewer__username','reviewed__reviewer').\
                    exclude(id__in=reviewed).filter(date=selected_date).\
                    filter(user=name).order_by('-id')
            else:
                if super_user_allow == 1 or self.user.is_superuser:
                    open_for_review = DailyReport.objects.values('id','user','user__username',
                        'project__project__title','project__project__manager','date',
                        'reviewed','reviewed__is_claimed',
                        'reviewed__reviewer__username','reviewed__reviewer').\
                        exclude(id__in=reviewed).filter(date=selected_date).order_by('-id')
                else:
                    if manager_allow == 1:
                        super_user_list = User.objects.values_list('id', flat=True).\
                        filter(groups__name='super_user')
                        open_for_review = DailyReport.objects.values('id','user','user__username',
                            'project__project__title','project__project__manager','date',
                            'reviewed','reviewed__is_claimed',
                            'reviewed__reviewer__username','reviewed__reviewer').\
                            exclude(id__in=reviewed).filter(date=selected_date).order_by('-id').\
                            exclude(user__in=super_user_list)
                    else:
                        super_user_list = User.objects.values_list('id', flat=True).\
                        filter(groups__name='super_user')
                        manager_list = User.objects.values_list('id', flat=True).\
                        filter(groups__name='managers')
                        open_for_review = DailyReport.objects.values('id','user','user__username',
                            'project__project__title','project__project__manager','date',
                            'reviewed','reviewed__is_claimed',
                            'reviewed__reviewer__username','reviewed__reviewer').\
                            exclude(id__in=reviewed).filter(date=selected_date).order_by('-id').\
                            exclude(user__in=super_user_list).exclude(user__in=manager_list)

            temp = Context({'open':open_for_review, 'user_id':request.user.id,
                'access_var':access_var,'notice_status':notice_status,
                'date':selected_date})
            content = get_template('main/review_select_result.html')
            html_content = content.render(temp)
            return HttpResponse(html_content)
        elif 'name' in request.GET:
            name = request.GET['name']
            reviewed = Reviewed.objects.values_list('id').filter(is_reviewed=True)
            if normal_user_allow == 1:
                manager_list = ProjectDetails.objects.values_list('manager', flat=True).filter()
                open_for_review = DailyReport.objects.values('id','user','user__username',
                    'project__project__title','project__project__manager','date','reviewed',
                    'reviewed__is_claimed', 'reviewed__reviewer__username','reviewed__reviewer').\
                    exclude(id__in=reviewed).filter(user=name).order_by('-id').\
                    exclude(user__in=manager_list)
            else:
                open_for_review = DailyReport.objects.values('id','user','user__username',
                    'project__project__title','project__project__manager','date','reviewed',
                    'reviewed__is_claimed', 'reviewed__reviewer__username','reviewed__reviewer').\
                    exclude(id__in=reviewed).filter(user=name).order_by('-id')

            temp = Context({'open':open_for_review, 'user_id':request.user.id,
                'access_var':access_var,'notice_status':notice_status})
            content = get_template('main/review_select_result.html')
            html_content = content.render(temp)
            return HttpResponse(html_content)
        else:
            superuser = request.user.is_superuser
            form = DateSelectForm(super_user_allow, manager_allow, normal_user_allow, superuser)
            return render(request,'main/review.html',{'form':form})


def maintainer(request):
    try:
        maintainer = request.user.id
        return HttpResponse(maintainer)
    except:
        return HttpResponse('0')

def maintenance(request):
    return HttpResponse("<h1>Site Under Maintenance</h1>")


@login_required
def members(request):
    """
    Function that return list of project member in json format.
    """
    if 'project_id' in request.GET:
        project_id = request.GET['project_id']
        user_obj = User.objects.filter(teammembers__project__id=project_id).\
            order_by('username')
    else:
        user_obj = User.objects.all().order_by('username')
    members = {}
    for user_val in user_obj:
        members['_' + str(user_val.id)] = user_val.username

    final_dict = OrderedDict(sorted(members.items(), key=lambda t: t[1].lower()))
    return HttpResponse(simplejson.dumps(final_dict))


class TimelyReports(View):
    """
    Class to handel request for generating timely reports. User can 
    generate monthly ,weekly or specific daterange functionality.
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TimelyReports, self).dispatch(*args, **kwargs)

    def __init__(self):
        pass

    def get(self, request):
        """
        Handels get request for TimelyReports class.
        Returns form for displaying daterangeselection.
        """
        manager=request.user
        super_user = is_super_user(request)
        form = DateRangeSelectionForm(manager, super_user)
        access_var = is_manager(request)
        notice_status = read_unread_notice(request)
        return render(request, 'main/daterangeselection.html', {'form':form,
            'access_var':access_var, 'notice_status':notice_status})

    def post(self, request):
        """
        Handels post request for TimelyReports.
        Return rendered report for selected credentials.
        """
        manager = request.user.id
        super_user = is_super_user(request)
        form = DateRangeSelectionForm(manager, super_user, request.POST)
        if form.is_valid():
            report_type = request.POST['report_type']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            if report_type == '1':
                members = request.POST['members']
                project_id = request.POST['project']
                project_name = ProjectDetails.objects.filter(id=project_id)[0]
                username = User.objects.filter(id=members)[0]
                var_list = DailyReportItem.objects.filter(daily_report__user=members,
                    daily_report__date__range=(start_date,end_date),
                    daily_report__project__project=project_id).values(
                    'daily_report__rating__rating', 'self_rating', 'work_done',
                    'struggle', 'duration_in_hours', 'tags', 'daily_report__date'
                    ).order_by('-daily_report__date')
                duration_list = DailyReportItem.objects.filter(daily_report__user=members,
                    daily_report__date__range=(start_date,end_date),
                    daily_report__project__project=project_id).values_list(
                    'duration_in_hours', flat=True)
                total_hours = hours(*duration_list)
                total_minutes = minutes(*duration_list)
                return render(request, 'main/timely_report.html', {'var_list':var_list,
                    'access_var':access_var, 'notice_status':notice_status,
                    'report_type':report_type, 'project_name':project_name,
                    'start_date':start_date, 'end_date':end_date,
                    'username':username, 'total_hours':total_hours, 'total_minutes':total_minutes})
            elif report_type == '2':
                project_id = request.POST['project']
                project_name = ProjectDetails.objects.filter(id=project_id)[0]
                var_list = DailyReportItem.objects.filter(
                    daily_report__date__range=(start_date,end_date),
                    daily_report__project__project=project_id).values(
                    'daily_report__rating__rating', 'self_rating', 'work_done',
                    'struggle', 'duration_in_hours', 'tags',
                    'daily_report__user__username', 'daily_report__date'
                    ).order_by('daily_report__user')
                duration_list = DailyReportItem.objects.filter(
                    daily_report__date__range=(start_date,end_date),
                    daily_report__project__project=project_id).values_list(
                    'duration_in_hours', flat=True)
                total_hours = hours(*duration_list)
                total_minutes = minutes(*duration_list)
                return render(request, 'main/timely_report.html', {'var_list':var_list,
                    'access_var':access_var, 'notice_status':notice_status,
                    'report_type':report_type, 'project_name':project_name,
                    'start_date':start_date, 'end_date':end_date,
                    'total_hours':total_hours, 'total_minutes':total_minutes})
            elif report_type == '3':
                members = request.POST['members']
                username = User.objects.filter(id=members)[0]
                var_list = DailyReportItem.objects.filter(daily_report__user=members,
                    daily_report__date__range=(start_date,end_date)).values(
                    'daily_report__rating__rating', 'self_rating', 'work_done',
                    'struggle', 'duration_in_hours', 'tags',
                    'daily_report__user__username', 'daily_report__date',
                    'daily_report__project__project__title'
                    ).order_by('daily_report__date', 'daily_report__project__project__title')
                duration_list = DailyReportItem.objects.filter(daily_report__user=members,
                    daily_report__date__range=(start_date,end_date)).values_list(
                    'duration_in_hours', flat=True)
                total_hours = hours(*duration_list)
                total_minutes = minutes(*duration_list)
                return render(request, 'main/timely_report.html', {'var_list':var_list,
                    'access_var':access_var, 'notice_status':notice_status,
                    'report_type':report_type, 'start_date':start_date,
                    'end_date':end_date, 'username':username,
                    'total_hours':total_hours, 'total_minutes':total_minutes})
        else:
            manager=request.user
            form = DateRangeSelectionForm(manager, super_user,request.POST)
            access_var = is_manager(request)
            notice_status = read_unread_notice(request)
            return render(request, 'main/daterangeselection.html', {'form':form,
                'access_var':access_var, 'notice_status':notice_status})

class EditReport(View):
    """
    Class that enables editing of report.
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditReport, self).dispatch(*args, **kwargs)

    def get(self, request):
        """
        Handels get request.
        """
        self.report_id  = request.GET['report_id']
        self.report_obj = DailyReport.objects.get(id=self.report_id)
        self.user = request.user
        if self.report_obj.user.id == self.user.id:
            self.prepare_form(request)
            return render(request, 'users/edit_report.html',{'repot_form':
                self.add_report_form,'report_item':self.report_item_form_list,
                'report_id':self.report_id})

        else:
            return render(request, 'access_denied.html',{})

    def prepare_form(self, request):
        """
        Prepare forms for editing.
        """
        self.add_report_form = AddReportForm(self.user,instance=self.report_obj)
        self.report_item_form_list = []
        report_item_list = DailyReportItem.objects.values_list('id',flat=True).\
            filter(daily_report=self.report_id)

        if report_item_list:
            for item in report_item_list:
                report_item = DailyReportItem.objects.get(id=item)
                report_item_form = ReportItemForm(None, instance=report_item)
                self.report_item_form_list.append(report_item_form)
        else:
            report_item_form = ReportItemForm()
            self.report_item_form_list.append(report_item_form)

    def post(self, request):
        """
        Handels post request.
        """
        self.report_id = request.GET['report_id']
        self.report_obj = DailyReport.objects.get(id=self.report_id)
        self.remove_garbage(request)
        self.save_new_values(request)
        message="Changes Saved"
        return render(request,'users/report_success.html',{'message':message})


    def remove_garbage(self,request):
        """
        Remove garbage(previous) values.
        """
        report_item_list = DailyReportItem.objects.values_list('id',flat=True).\
            filter(daily_report=self.report_id)
        for item in report_item_list:
            report_item = DailyReportItem.objects.get(pk=item)
            report_item.delete()

    def save_new_values(self,request):
        """
        Save new values for selected report.
        """
        user = request.user
        reportform = AddReportForm(user, request.POST)
        reportitemform = ReportItemForm(request.POST)
        if reportform.is_valid() and reportitemform.is_valid():
            user = request.user
            project = ProjectDetails.objects.get(teammembers=request.POST['project'])
            team_id = TeamMembers.objects.values_list('id',flat=True).\
                filter(project=project.id).filter(user=user.id)[0]
            team_obj = TeamMembers.objects.get(pk=team_id)
            DailyReport.objects.filter(id=self.report_id).update(project=team_obj)
            self_rating_list = request.POST.getlist('self_rating')
            duration_list = request.POST.getlist('duration_in_hours')
            work_done_list = request.POST.getlist('work_done')
            struggle_list = request.POST.getlist('struggle')
            tags_list = request.POST.getlist('tags')
            i = 0
            for self_rate in self_rating_list:
                reportitemobj = DailyReportItem(daily_report=self.report_obj,
                    self_rating=self_rate, duration_in_hours=duration_list[i],
                    work_done=work_done_list[i], struggle=struggle_list[i],
                    tags=tags_list[i])
                reportitemobj.save()
                i = i + 1

class TimeTracking(View):
    """Class that handels time tracking."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TimeTracking, self).dispatch(*args, **kwargs)

    def get(self, request):
        """Handels get request."""
        self.user = request.user
        if 'start_stop_time' in request.GET:
            self.add_data(request)

        if 'get_time' in request.GET:
            return self.get_time(request)

        if 'timer_status' in request.GET:
            return self.timer_status(request)

        if 'reset' in request.GET:
            return self.reset_timer(request)

        if 'pause' in request.GET:
            return self.pause_timer(request)

        if 'get_work_done' in request.GET:
            return self.get_work_done(request)

        time = TimeTrackingData.objects.filter(user=self.user.id)
        if time:
            now = datetime.datetime.utcnow().replace(tzinfo = pytz.utc)
            time_obj = TimeTrackingData.objects.get(user=self.user.id)
            if time_obj.end_time:
                timer_stoped = 1
                timer_status = 0
                timer_paused = 0
                self.total_seconds = (time_obj.end_time-time_obj.start_time).\
                    total_seconds()
            else:
                pause = PauseTimer.objects.filter(user=self.user.id)
                if pause:
                    paused_seconds = self.calculate_paused_seconds(request)
                    self.total_seconds = (now-time_obj.start_time).\
                    total_seconds() - paused_seconds
                    currently_paused = PauseTimer.objects.filter(user=self.user.id).\
                    filter(currenlty_paused=True)
                    if currently_paused:
                        timer_paused = 1
                    else:
                        timer_paused = 0
                else:
                    self.total_seconds = (now-time_obj.start_time).\
                    total_seconds()
                    timer_paused = 0
                timer_stoped = 0
                timer_status = 1
                
            time_minutes_elapsed = int(self.total_seconds/60)
            hours = time_minutes_elapsed/60
            minutes = int((time_minutes_elapsed/float(60) - hours)*60)
            seconds = int(self.total_seconds - hours*3600 - minutes*60)
            hours = str(hours).zfill(2)
            minutes = str(minutes).zfill(2)
            seconds = str(seconds).zfill(2)
            time_string = hours + ':' + minutes + ':' + seconds

        else:
            timer_paused = 0
            timer_stoped = 0
            timer_status = 0
            time_string = '00:00:00'
        reportform = AddReportForm(initial={'user':self.user}, pro=self.user)
        reportitemform = ReportItemForm()
        return render(request,'main/time_track.html',{'reportform':reportform,
            'reportitem':reportitemform,'time_string':time_string,
            'timer_status':timer_status,'timer_stoped':timer_stoped,
            'timer_paused':timer_paused})

    def calculate_paused_seconds(self, request):
        paused = PauseTimer.objects.values('start_time','end_time').\
            filter(user=self.user)
        total_paused_seconds = 0
        for value in paused:
            if value['end_time']:
                end_time = value['end_time']
            else:
                end_time = datetime.datetime.utcnow().replace(tzinfo = pytz.utc)

            seconds = (end_time-value['start_time']).total_seconds()
            total_paused_seconds = total_paused_seconds + seconds

        return total_paused_seconds


    def add_data(self, request):
        user_data = TimeTrackingData.objects.filter(user=self.user.id)
        now = datetime.datetime.utcnow().replace(tzinfo = pytz.utc)
        if user_data:
            user_data.update(end_time=datetime.datetime.now())
            try:
                paused = PauseTimer.objects.filter(user=self.user).\
                filter(currenlty_paused = True).update(currenlty_paused=False, 
                    end_time=now)
            except:
                pass

        else:
            try:
                work_done = request.GET['work']
            except:
                work_done = ''
            UserOfTimer(user=self.user).save()
            TimeTrackingData(start_time=now,user=self.user,work_done=work_done).save()

    def timer_status(self, request):
        try:
            time = TimeTrackingData.objects.get(user=self.user.id)
        except:
            time = ''
        if time:
            return HttpResponse('1')
        else:
            return HttpResponse('0')

    def get_work_done(self,request):
        data = TimeTrackingData.objects.get(user=self.user.id)
        return HttpResponse(data.work_done)

    def get_time(self,request):
        time_obj = TimeTrackingData.objects.get(user=self.user.id)
        paused_seconds = self.calculate_paused_seconds(request)
        time_minutes_elapsed = int(((time_obj.end_time-time_obj.start_time).\
            total_seconds()-paused_seconds)/60)
        hours = time_minutes_elapsed/60
        minutes = str(int((time_minutes_elapsed/float(60) - hours)*60)).zfill(2)
        hours = str(hours).zfill(2)
        time_string = hours + ':' + minutes
        return HttpResponse(time_string)

    def post(self, request):
        self.user = request.user
        reportform = AddReportForm(self.user, request.POST)
        reportitemform = ReportItemForm(request.POST)
        timer_status = '0'
        
        if reportform.is_valid() and reportitemform.is_valid():
            project = request.POST['project']
            report_id = DailyReport.objects.values_list('id',flat=True).filter(user=self.user.id).\
                filter(project=project).filter(date=datetime.date.today())
            if report_id:
                reportformdata = DailyReport.objects.get(pk=report_id[0])
            else:
                reportformdata = reportform.save()
            cd = reportitemform.cleaned_data
            self_rating = cd['self_rating']
            duration = cd['duration_in_hours']
            work_done = cd['work_done']
            struggle = cd['struggle']
            tags = cd['tags']
            reportitemformdata = DailyReportItem(daily_report=reportformdata,
                self_rating=self_rating, duration_in_hours=duration,
                work_done=work_done, struggle=struggle, tags=tags)
            reportitemformdata.save()
            message = "Report Added"
            self.reset_timer(request)
            try:
                time = TimeTrackingData.objects.get(user=self.user.id)
            except:
                time = ''
            dailyreportobject = DailyReport.objects.get(pk=reportformdata.id)
            dailyreportobj = DailyReport.objects.values('project__project__manager').\
            filter(id=reportformdata.id)[0]
            user_obj = User.objects.get(pk=dailyreportobj['project__project__manager'])
            if self.user != user_obj:
                notification_type = NotificationType.objects.get(name='Report')
                notifications = Notifications(notification_type=notification_type)
                notifications.save()
                notifications_obj = Notifications.objects.get(id=notifications.id)
                report_notifications = ReportNotifications(report=dailyreportobject,
                    notifier=user_obj, notifications=notifications_obj)
                report_notifications.save()
                try:
                    if time:
                        timer_status = '1'
                    else:
                        timer_status = '0'
                except:
                    pass

            return render(request,'users/report_success.html',{'message':message,
                'status':timer_status})
        else:
            reportform = AddReportForm(self.user, request.POST)
            reportitemform = ReportItemForm(request.POST)
            timer_stoped = 1
            timer_status = 0
            return render(request,'main/time_track.html',{'reportform':reportform,
            'reportitem':reportitemform,'timer_status':timer_status,
            'timer_stoped':timer_stoped})

    def reset_timer(self,request):
        time_track = TimeTrackingData.objects.get(user=self.user.id)
        time_track.delete()
        paused = PauseTimer.objects.values_list('id',flat=True).filter(user=self.user)
        for value in paused:
            PauseTimer.objects.get(pk=value).delete()
        return HttpResponse('1')

    def pause_timer(self,request):
        try:
            paused = PauseTimer.objects.filter(user=self.user).\
                filter(currenlty_paused = True)
        except:
            paused = ''
        now = datetime.datetime.utcnow().replace(tzinfo = pytz.utc)
        if paused:
            paused = PauseTimer.objects.filter(user=self.user).\
                filter(currenlty_paused = True).update(currenlty_paused=False, 
                    end_time=now)

        else:
            PauseTimer(start_time=now, user=self.user).save()

        return HttpResponse('paused')

def delete_report(request):
    """function that handels delete report request."""
    report_id = request.GET['report_id']
    user = request.user
    report = DailyReport.objects.get(pk=report_id)
    report_items = DailyReportItem.objects.values_list('id', flat=True).\
        filter(daily_report=report_id)
    if user.id == report.user.id:
        for value in report_items:
            DailyReportItem.objects.get(pk=value).delete()
        report.delete()
        return HttpResponse('1')
    else:
        return HttpResponse('2')


def hours(*args):
    total_time_minutes = 0
    total_hours = 0
    for value in args:
        time_temp = value.split(':')
        time_temp[0] = int(time_temp[0]) * 60
        try:
            total_time_minutes = int(time_temp[0]) + int(time_temp[1]) + total_time_minutes
        except:
            total_time_minutes = int(time_temp[0]) + total_time_minutes
        total_hours = total_time_minutes/60
    return total_hours


def minutes(*args):
    total_time_minutes = 0
    total_minutes = 0
    for value in args:
        time_temp = value.split(':')
        time_temp[0] = int(time_temp[0]) * 60
        try:
            total_time_minutes = int(time_temp[0]) + int(time_temp[1]) + total_time_minutes
        except:
            total_time_minutes = int(time_temp[0]) + total_time_minutes
        total_minutes = total_time_minutes%60
    return total_minutes

def restart_timer(request):
    TimeTracking.as_view()(request)
    return HttpResponseRedirect(reverse('time_tracking'))
