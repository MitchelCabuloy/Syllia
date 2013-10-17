from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
   # url(r'^accounts/', include('accounts.urls', namespace="accounts")),
   url(r'^$', TemplateView.as_view(template_name='home/index.html'), name='index'),
   url(r'^about/$', TemplateView.as_view(template_name='home/about.html'), name='about'),
   url(r'^contact/$', TemplateView.as_view(template_name='home/contact.html'), name='contact'),
   url(r'^syllabus/', include('syllabus.urls', namespace='syllabus')),
   url(r'^accounts/', include('authtools.urls', namespace='authtools')),
   url(r'^accounts/', include('accounts.urls', namespace='accounts')),
)
