# Create your views here.

from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.utils import simplejson, timezone
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from Syllia.apps.syllabus.models import Rubric, College, Department, Syllabus
from Syllia.apps.accounts.forms import ProfileForm
from Syllia.apps.syllabus.forms import FeedbackForm


# import logging

# Log everything, and send it to stderr.
# logging.basicConfig(level=logging.DEBUG)

class DashboardView(View):
    template_name = 'syllabus/dashboard.html'

    def get(self, request, *args, **kwargs):
        # If not authenticated, show home page
        if not request.user.is_authenticated():
            return render(request, 'home/index.html', {'home_page': True})

        # Else. Dashboard
        current_user = get_user_model().objects.get(
            email=request.user.email)

        # TODO: Make more DRY
        syllabus_set = current_user.syllabus_set.all()
        syllabusList = []

        for syllabus in syllabus_set:
            syllabusList.append({
                "pk": syllabus.id,
                "url": 'syllabus',
                "itemName": syllabus.syllabus_name,
                "lastModified": format_last_modified_time(syllabus.last_modified)
            })

        rubric_set = current_user.rubric_set.all()
        rubricList = []

        for rubric in rubric_set:
            rubricList.append({
                "pk": rubric.id,
                "url": 'rubric',
                "itemName": rubric.rubric_name,
                "lastModified": format_last_modified_time(rubric.last_modified)
            })

        profileData = {
            "college": current_user.faculty.department.college.id,
            "department": current_user.faculty.department.id
        }

        jsonData = {
            "syllabusList": syllabusList,
            "rubricList": rubricList,
            "collegeList": get_college_list(),
            "departmentList": get_department_list(),
            "profileData": profileData
        }

        context = {
            'jsonData': simplejson.dumps(jsonData)
        }

        # Load profile form
        if request.session.get('profile_form'):
            context['profile_form'] = request.session['profile_form']
            del request.session['profile_form']
        else:
            context['profile_form'] = ProfileForm(initial={
                'name': current_user.get_full_name()
            })

        # Load change password form
        if request.session.get('change_password_form'):
            context['change_password_form'] = request.session[
                'change_password_form']
            del request.session['change_password_form']
        else:
            context['change_password_form'] = PasswordChangeForm(current_user)

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
                jsonData['syllabusData'] = syllabus.json_data

                # Load modified time data
                jsonData['timeSinceModified'] = get_time_since_modified(
                    syllabus.last_modified)

            except Exception:
                raise Http404

        rubricList = []
        rubrics = current_user.rubric_set.all()

        for rubric in rubrics:
            rubricList.append(rubric.json())

        jsonData['rubricList'] = rubricList

        jsonData['collegeList'] = get_college_list()
        jsonData['departmentList'] = get_department_list()

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

        try:
            # Initialize
            syllabus.user = current_user
            syllabus.syllabus_name = json_data['syllabusName']
            syllabus.course_code = json_data['courseCode']
            syllabus.json_data = json_data

            # Load foreign keys
            # These will throw an exception if invalid
            syllabus.department = Department.objects.get(
                pk=json_data['department'])
            if('rubric' in json_data):
                syllabus.rubric = current_user.rubric_set.get(
                    pk=json_data['rubric'])

            syllabus.save()

            response_data = {
                'viewModel': syllabus.json_data,
                'timeSinceModified': get_time_since_modified(syllabus.last_modified)
            }

            if request.POST['redirect'] == "true":
                messages.success(request, 'Saved syllabus')
                response_data['redirectTo'] = reverse('index')

            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        except Exception:
            return HttpResponseServerError(simplejson.dumps({'message': 'You must at least have basic information before saving.'}), content_type="application/json")


@csrf_protect
@login_required
def delete_syllabus(request):
    if request.method == "POST":
        item_ids = request.POST.getlist('ids_json[]')

        response_data = {}
        current_user = get_user_model().objects.get(
            email=request.user.email)

        try:
            current_user.syllabus_set.filter(id__in=item_ids).delete()
            response_data['success'] = True
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        except Exception:
            return HttpResponseServerError(simplejson.dumps({'message': 'Something went wrong.'}), content_type="application/json")


class RubricView(View):
    template_name = 'syllabus/rubric.html'

    def get(self, request, *args, **kwargs):
        if(len(args)):
            current_user = get_user_model().objects.get(
                email=request.user.email)

            try:
                rubric = current_user.rubric_set.get(pk=args[0])

                jsonData = {
                    'rubricData': rubric.json_data,
                    'timeSinceModified': get_time_since_modified(rubric.last_modified)
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

        try:
            rubric.user = current_user
            rubric.rubric_name = json_data['rubricName']
            rubric.json_data = json_data

            rubric.save()

            messages.success(request, 'Saved rubric')
            return redirect('index')
        except Exception:
            jsonData = {
                'rubricData': json_data
            }

            context = {'jsonData': simplejson.dumps(jsonData)}
            messages.error(request, 'Please check your forms')
            return render(request, self.template_name, context)


@csrf_protect
@login_required
def delete_rubric(request):
    if request.method == "POST":
        item_ids = request.POST.getlist('ids_json[]')

        response_data = {}
        current_user = get_user_model().objects.get(
            email=request.user.email)

        try:
            current_user.rubric_set.filter(id__in=item_ids).delete()
            response_data['success'] = True
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        except Exception:
            return HttpResponseServerError(simplejson.dumps({'message': 'Something went wrong.'}), content_type="application/json")


class FeedbackView(View):
    template_name = 'home/feedback.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, 'home/feedback_thanks.html')

        return render(request, 'home/feedback.html', {'form': form})


# static methods
def format_last_modified_time(last_modified):
    if timezone.localtime(last_modified).date() == timezone.localtime(datetime.utcnow().replace(tzinfo=timezone.utc)).date():
        last_modified_string = timezone.localtime(
            last_modified).strftime('%I:%M %p')
    else:
        last_modified_string = timezone.localtime(
            last_modified).strftime('%b %d')

    return last_modified_string


def get_time_since_modified(last_modified):
    time_since_modified = datetime.utcnow().replace(
        tzinfo=timezone.utc) - last_modified
    s = time_since_modified.total_seconds()
    days, remainder = divmod(s, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # If less than an hour, show minutes ago
    if time_since_modified < timedelta(minutes=60):
        time_since_modified_string = "%d minutes" % minutes
    elif time_since_modified < timedelta(hours=24):
        time_since_modified_string = "%d hours" % hours
    else:
        time_since_modified_string = "%d days" % days

    return time_since_modified_string


def get_college_list():
    collegeList = []
    colleges = College.objects.all()
    for college in colleges:
        collegeList.append(college.json())

    return collegeList


def get_department_list():
    departmentList = []
    departments = Department.objects.all()
    for department in departments:
        departmentList.append(department.json())

    return departmentList
