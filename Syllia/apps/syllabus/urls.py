from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from Syllia.apps.syllabus import views, pdf

urlpatterns = patterns('',
    # url(r'^$', login_required(DashboardView.as_view()), name='index'),
    url(r'^syllabus/new/$', login_required(views.SyllabusView.as_view()), name='syllabus'),
    url(r'^syllabus/(\d+)/$', login_required(views.SyllabusView.as_view()), name='syllabus'),
    url(r'^syllabus/delete/$', views.delete_syllabus, name='delete_syllabus'),
    url(r'^rubric/new/$', login_required(views.RubricView.as_view()), name='rubric'),
    url(r'^rubric/(\d+)/$', login_required(views.RubricView.as_view()), name='rubric'),
    url(r'^rubric/delete/$', views.delete_rubric, name='delete_rubric'),
    url(r'^pdf/$', pdf.return_a_pdf, name='pdf'),
    url(r'^feedback/$', login_required(views.FeedbackView.as_view()), name='feedback'),
)
