# Create your views here.

from datetime import datetime

from django.contrib.auth import get_user_model
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import simplejson

from syllabus.models import Rubric, College, Department, Syllabus


class DashboardView(View):
    template_name = 'syllabus/dashboard.html'

    def get(self, request, *args, **kwargs):
        # If not authenticated, show home page
        if not request.user.is_authenticated():
            return render(request, 'home/index.html')

        syllabus = Syllabus.objects.all()
        context = {'syllabus': syllabus}
        return render(request, self.template_name, context)


class SyllabusView(View):
    template_name = 'syllabus/syllabus.html'

    def get(self, request, *args, **kwargs):
        current_user = get_user_model().objects.get(
            email=request.user.email)

        rubricList = []
        rubrics = current_user.rubric_set.all()

        for rubric in rubrics:
            rubricList.append(rubric.json())

        # Create dictionary
        context = {
            'rubricList': simplejson.dumps(rubricList)
        }

        collegeList = []
        colleges = College.objects.all()
        for college in colleges:
            collegeList.append(college.json())

        context['collegeList'] = simplejson.dumps(collegeList)

        departmentList = []
        departments = Department.objects.all()
        for department in departments:
            departmentList.append(department.json())

        context['departmentList'] = simplejson.dumps(departmentList)

        # If edit mode, load syllabus data
        if(len(args)):
            try:
                syllabus = current_user.syllabus_set.get(pk=args[0])

                context['jsonString'] = syllabus.json_data

                # return render(request, self.template_name, context)

            except Exception:
                raise Http404

        # If reached here, no arguments. Return empty form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Deserialize to dictionary
        json_data = simplejson.loads(request.POST['syllabus_json'])

        current_user = get_user_model().objects.get(email=request.user.email)

        # Load or create new syllabus
        try:
            syllabus = current_user.syllabus_set.get(pk=int(json_data['pk']))
        except Exception:
            syllabus = Syllabus()

        # Initialize
        syllabus.user = current_user
        syllabus.course_code = json_data['courseCode']
        syllabus.json_data = request.POST['syllabus_json']

        # Load foreign keys
        # These will throw an exception if invalid
        syllabus.department = Department.objects.get(
            pk=json_data['department'])
        syllabus.rubric = current_user.rubric_set.get(pk=json_data['rubric'])

        syllabus.save()

        return HttpResponse(syllabus.json_data)


class RubricView(View):
    template_name = 'syllabus/rubric.html'

    def get(self, request, *args, **kwargs):
        if(len(args)):
            current_user = get_user_model().objects.get(
                email=request.user.email)

            try:
                rubric = current_user.rubric_set.get(pk=args[0])
                context = {'jsonString': rubric.json_data}
                return render(request, self.template_name, context)
            except Exception:
                raise Http404

        # If reached here, no arguments. Return empty form
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Deserialize
        json_data = simplejson.loads(request.POST['rubric_json'])

        current_user = get_user_model().objects.get(email=request.user.email)

        rubric = None
        try:
            rubric = current_user.rubric_set.get(pk=int(json_data['pk']))
        except Exception:
            rubric = Rubric()

        rubric.user = current_user
        rubric.rubric_name = json_data['rubricName']
        rubric.json_data = request.POST['rubric_json']

        rubric.save()

        return HttpResponse(rubric.json_data)
