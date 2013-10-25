from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from syllabus.views import SyllabusView, DashboardView, RubricView

urlpatterns = patterns('',
    # url(r'^$', login_required(DashboardView.as_view()), name='index'),
    url(r'^syllabus/new/$', login_required(SyllabusView.as_view()), name='syllabus'),
    url(r'^syllabus/(\d+)/$', login_required(SyllabusView.as_view()), name='syllabus'),
    url(r'^rubric/new/$', login_required(RubricView.as_view()), name='rubric'),
    url(r'^rubric/(\d+)/$', login_required(RubricView.as_view()), name='rubric'),
    # url(r'^profile/$', ProfileView.as_view(), name='profile'),
    # url(r'^register/$', RegisterView.as_view(), name='register'),
)
