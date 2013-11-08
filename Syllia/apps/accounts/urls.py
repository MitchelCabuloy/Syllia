from django.conf.urls import patterns, url

from Syllia.apps.accounts import views

urlpatterns = patterns('',
   url(r'^register/$', views.RegisterView.as_view(), name='register'),
   url(r'^update_profile/$', views.update_profile, name='update_profile'),
   url(r'^change_password/$', views.change_password, name='change_password'),
)
