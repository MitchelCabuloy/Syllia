from django.conf.urls import patterns, url

from Syllia.apps.accounts.views import ProfileView, RegisterView, change_password

urlpatterns = patterns('',
   url(r'^register/$', RegisterView.as_view(), name='register'),
   url(r'^profile/$', ProfileView.as_view(), name='profile'),
   url(r'^change_password/$', change_password, name='change_password'),
)
