from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   # url(r'^accounts/', include('accounts.urls', namespace="accounts")),
   url(r'^accounts/', include('authtools.urls', namespace='accounts')),
   url(r'^accounts/', include('accounts.urls', namespace='accounts')),
)
