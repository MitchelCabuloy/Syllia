from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from syllabus.views import DashboardView

urlpatterns = patterns('',
   # url(r'^accounts/', include('accounts.urls', namespace="accounts")),
   # url(r'^$', TemplateView.as_view(template_name='home/index.html'), name='index'),

   # Syllabus App
   url(r'^$', DashboardView.as_view(), name='index'),
   url(r'^', include('syllabus.urls', namespace='syllabus')),

   # Static pages
   url(r'^about/$', TemplateView.as_view(template_name='home/about.html'), name='about'),
   url(r'^contact/$', TemplateView.as_view(template_name='home/contact.html'), name='contact'),
   # url(r'^rubric/$', TemplateView.as_view(template_name='home/rubric.html'), name='rubric'),
   # url(r'^dashboard/$', TemplateView.as_view(template_name='home/dashboard.html'), name='dashboard'),

   # Accounts and authentication
   url(r'^accounts/', include('authtools.urls', namespace='authtools')),
   url(r'^accounts/', include('accounts.urls', namespace='accounts')),
)
