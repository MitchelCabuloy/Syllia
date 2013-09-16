# Create your views here.

from django.contrib.auth import get_user_model
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from syllabus.models import Syllabus


class DashboardView(View):
    template_name = 'syllabus/dashboard.html'

    def get(self, request, *args, **kwargs):
        syllabus = Syllabus.objects.all()
        context = {'syllabus': syllabus}
        return render(request, self.template_name, context)

class AddSyllabusView(View):
    template_name = 'syllabus/add.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        json = request.POST['syllabus_json']
        # do stuff
        return HttpResponseRedirect(reverse('syllabus:dashboard'))
