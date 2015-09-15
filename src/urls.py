from django.conf.urls import patterns, include, url
from django.contrib import admin
from src.main.views import MainIndex, SignUp, ViewReport
from src.managers.views import Project, AddTeam, ProjectOptions
from src.users.views import AddReport, UserProfile
from src.main.views import Comment, Review, TimelyReports, EditReport
from src.main.views import TimeTracking
from src.notifications.views import Notification

urlpatterns = patterns('',
    # Examples:
    url(r'^$', MainIndex.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^maintainer/','src.main.views.maintainer', name='maintainer'),
    url(r'^maintenance', 'src.main.views.maintenance', name='maintenance'),
    url(r'^project', Project.as_view(), name='project'),
    url(r'^options', ProjectOptions.as_view(), name='project_options'),
    url(r'^add_team', AddTeam.as_view(), name='add_team'),
    url(r'^signup/$', SignUp.as_view(),
        name='signup_view'),

    url(r'^signin/$', 'django.contrib.auth.views.login',
        {'template_name': 'registration/login_form.html',
        'redirect_field_name' : '/' },
        name='signin'),

    url(r'^signout/$','django.contrib.auth.views.logout',
        {'next_page' : '/signin'}, name='signout'),
    url(r'^view_report', ViewReport.as_view(), name='view_report'),
    url(r'^report', AddReport.as_view(), name='report'),
    url(r'^access_denied', 'src.managers.views.access_denied'),
    url(r'^password_change', 'src.main.views.password_change'),
    url(r'^comment', Comment.as_view(), name='comment' ),
    url(r'^jsreverse/', 'src.main.views.jsreverse'),
    url(r'^review', Review.as_view(), name='review'),
    url(r'^notification', Notification.as_view(), name='notification'),
    url(r'^user_profile', UserProfile.as_view(), name='user_profile'),
    url(r'^timely_reports', TimelyReports.as_view(), name='timely_reports'),
    url(r'^edit_report', EditReport.as_view(), name='edit_report'),
    url(r'^time_tracking', TimeTracking.as_view(), name='time_tracking'),
    url(r'^members', 'src.main.views.members'),
    url(r'^delete_report', 'src.main.views.delete_report', name='delete_report'),
    url(r'^change_status', 'src.managers.views.change_status', name='change_status'),
    url(r'^view_history', 'src.managers.views.view_history', name='view_history'),
    url(r'^change_project_title', 'src.managers.views.change_project_title', name='change_project_title'),
    url(r'^restart_timer','src.main.views.restart_timer', name='restart_timer'),
)


