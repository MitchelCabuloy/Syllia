from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from syllabus.views import AddSyllabusView, DashboardView, RubricView

urlpatterns = patterns('',
    url(r'^$', login_required(DashboardView.as_view()), name='index'),
    url(r'^add/$', login_required(AddSyllabusView.as_view()), name='add'), # TODO: Change to just 'syllabus'
    url(r'^edit/(\d+)/$', login_required(AddSyllabusView.as_view()), name='edit'),
    url(r'^rubric/$', login_required(RubricView.as_view()), name='rubric'),
    url(r'^rubric/(\d+)/$', login_required(RubricView.as_view()), name='rubric'),
    # url(r'^profile/$', ProfileView.as_view(), name='profile'),
    # url(r'^register/$', RegisterView.as_view(), name='register'),
)
