from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from Syllia.apps.syllabus import views

urlpatterns = patterns('',
    # url(r'^$', login_required(DashboardView.as_view()), name='index'),
    url(r'^syllabus/new/$', login_required(views.SyllabusView.as_view()), name='syllabus'),
    url(r'^syllabus/(\d+)/$', login_required(views.SyllabusView.as_view()), name='syllabus'),
    url(r'^rubric/new/$', login_required(views.RubricView.as_view()), name='rubric'),
    url(r'^rubric/(\d+)/$', login_required(views.RubricView.as_view()), name='rubric'),
)
