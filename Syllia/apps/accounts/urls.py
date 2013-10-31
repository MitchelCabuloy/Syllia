from django.conf.urls import patterns, url

from Syllia.apps.accounts.views import RegisterView, change_password, update_profile

urlpatterns = patterns('',
   url(r'^register/$', RegisterView.as_view(), name='register'),
   url(r'^update_profile/$', update_profile, name='update_profile'),
   url(r'^change_password/$', change_password, name='change_password'),
)
