from django.conf.urls import patterns, url
from syllabus.views import AddSyllabusView, DashboardView

urlpatterns = patterns('',
    url(r'^$', DashboardView.as_view(), name='index'),
    url(r'^add/$', AddSyllabusView.as_view(), name='add'),
    # url(r'^profile/$', ProfileView.as_view(), name='profile'),
    # url(r'^register/$', RegisterView.as_view(), name='register'),
)
