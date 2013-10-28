# Create your views here.

from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import simplejson, timezone

from syllabus.models import Rubric, College, Department, Syllabus


class DashboardView(View):
    template_name = 'syllabus/dashboard.html'

    def get(self, request, *args, **kwargs):
        # If not authenticated, show home page
        if not request.user.is_authenticated():
            return render(request, 'home/index.html')

        # Else. Dashboard
        current_user = get_user_model().objects.get(
            email=request.user.email)

        # TODO: Make more DRY
        syllabus_set = current_user.syllabus_set.all()
        syllabusList = []

        for syllabus in syllabus_set:
            # Both in UTC
            if syllabus.last_modified.date() == datetime.utcnow().date():
                lastModified = timezone.localtime(syllabus.last_modified).strftime('%I:%M %p')
            else:
                lastModified = timezone.localtime(syllabus.last_modified).strftime('%b %d')

            syllabusList.append({
                "pk": syllabus.id,
                "url": 'syllabus',
                "itemName": syllabus.syllabus_name,
                "lastModified": lastModified
            })

        rubric_set = current_user.rubric_set.all()
        rubricList = []

        for rubric in rubric_set:
            # Both in UTC
            if rubric.last_modified.date() == datetime.utcnow().date():
                lastModified = timezone.localtime(rubric.last_modified).strftime('%I:%M %p')
            else:
                lastModified = timezone.localtime(rubric.last_modified).strftime('%b %d')

            rubricList.append({
                "pk": rubric.id,
                "url": 'rubric',
                "itemName": rubric.rubric_name,
                "lastModified": lastModified
            })

        jsonData = {
            "syllabusList": syllabusList,
            "rubricList": rubricList
        }

        context = {'jsonData': simplejson.dumps(jsonData)}
        return render(request, self.template_name, context)


class SyllabusView(View):
    template_name = 'syllabus/syllabus.html'

    def get(self, request, *args, **kwargs):
        current_user = get_user_model().objects.get(
            email=request.user.email)

        # Create dictionary
        jsonData = {}

        # If edit mode, load syllabus data
        if(len(args)):
            try:
                syllabus = current_user.syllabus_set.get(pk=args[0])
                jsonData['syllabusData'] = simplejson.loads(syllabus.json_data)

                # Load modified time data
                jsonData['timeSinceModified'] = get_last_modified_string(syllabus.last_modified)

            except Exception, e:
                print e.message
                raise Http404

        rubricList = []
        rubrics = current_user.rubric_set.all()

        for rubric in rubrics:
            rubricList.append(rubric.json())

        jsonData['rubricList'] = rubricList

        collegeList = []
        colleges = College.objects.all()
        for college in colleges:
            collegeList.append(college.json())

        jsonData['collegeList'] = collegeList

        departmentList = []
        departments = Department.objects.all()
        for department in departments:
            departmentList.append(department.json())

        jsonData['departmentList'] = departmentList

        # If reached here, no arguments. Return empty form
        return render(request, self.template_name, {"jsonData": simplejson.dumps(jsonData)})

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
        syllabus.syllabus_name = json_data['syllabusName']
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

                jsonData = {
                    'rubricData': simplejson.loads(rubric.json_data),
                    'timeSinceModified': get_last_modified_string(rubric.last_modified)
                }

                context = {'jsonData': simplejson.dumps(jsonData)}
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

# static methods

def get_last_modified_string(last_modified):
    time_since_modified = datetime.utcnow().replace(tzinfo=timezone.utc) - last_modified
    s = time_since_modified.total_seconds()
    days, remainder = divmod(s, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # If less than an hour, show minutes ago
    if time_since_modified < timedelta(minutes=60):
        timeSinceModified = "%d minutes" % minutes
    elif time_since_modified < timedelta(hours=24):
        timeSinceModified = "%d hours" % hours
    else:
        timeSinceModified = "%d days" % days

    return timeSinceModified
