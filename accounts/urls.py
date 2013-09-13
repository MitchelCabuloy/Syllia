from django.conf.urls import patterns, url

from accounts.views import ProfileView, RegisterView

urlpatterns = patterns('',
   url(r'^profile/$', ProfileView.as_view(), name='profile'),
   url(r'^register/$', RegisterView.as_view(), name='register'),
)
