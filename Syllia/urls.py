from django.conf.urls import patterns, include, url

from syllabus.views import DashboardView

urlpatterns = patterns('',
   # url(r'^accounts/', include('accounts.urls', namespace="accounts")),
   url(r'^$', DashboardView.as_view(), name='index'),
   url(r'^syllabus/', include('syllabus.urls', namespace='syllabus')),
   url(r'^accounts/', include('authtools.urls', namespace='authtools')),
   url(r'^accounts/', include('accounts.urls', namespace='accounts')),
)
