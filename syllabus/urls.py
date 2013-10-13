from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from syllabus.views import AddSyllabusView, DashboardView

urlpatterns = patterns('',
    url(r'^$', login_required(DashboardView.as_view()), name='index'),
    url(r'^add/$', login_required(AddSyllabusView.as_view()), name='add'),
    url(r'^edit/(\d+)/$', login_required(AddSyllabusView.as_view()), name='edit'),
    # url(r'^profile/$', ProfileView.as_view(), name='profile'),
    # url(r'^register/$', RegisterView.as_view(), name='register'),
)
