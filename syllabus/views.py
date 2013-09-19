# Create your views here.

from datetime import datetime

from django.contrib.auth import get_user_model
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils import simplejson

from syllabus.models import *


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
        self.process_json(request)
        # parsed_json = simplejson.loads('{"college":"College of Computer Studies","department":"Computer Technology","courseCode":"LBYFORE","courseName":"LBYFORE","courseDescription":"LBYFORE is a course that ahds-on laboratory component of FORENSC.","schedules":[{"days":"S","startTime":"1440","endTime":"1740"},{"days":"TH","startTime":"1300","endTime":"1600"}],"instructors":[{"firstName":"Cu","lastName":"Gregory"},{"firstName":"Pantola","lastName":"Alexi"}],"elgas":[{"elgaName":"Effective Communicator","learningOutcomes":[{"description":"LO 1: Be able to discuss different digital blah."}]},{"elgaName":"Critical/creative thinker","learningOutcomes":[{"description":"LO 2: Be able to gather artifact from different blah"},{"description":"LO 3: Be able to gather artifact from different operating systems"}]}],"finalCourseOutputDescription":"Final course output description here","requiredOutputs":[{"description":"Forensic Platform Preparation Report","weekDue":"4","los":["LO 1: Be able to discuss different digital blah."]},{"description":"Windows System and Artifacts Report","weekDue":"5","los":["LO 2: Be able to gather artifact from different blah","LO 3: Be able to gather artifact from different operating systems"]}],"otherOutputs":[{"requirementName":"Laboratory Exam"},{"requirementName":"Group Project"}],"gradingSystems":[{"itemName":"Laboratory Report Average","percentage":"60"},{"itemName":"Group Project","percentage":"20"},{"itemName":"Laboratory Exam","percentage":"20"}],"totalGradingSystem":100,"learningPlans":[{"topic":"Introduction / Orientation","weekNumber":"1","learningActivities":[{"description":"Course introduction"},{"description":"Classroom policies discussion"}],"los":[]},{"topic":"1.0 Forensic Platform Preparation","weekNumber":"3","learningActivities":[{"description":"Hands-on"}],"los":["LO 1: Be able to discuss different digital blah."]},{"topic":"2.0 Windows Systems and Artifacts","weekNumber":"4","learningActivities":[{"description":"Hands-on"}],"los":["LO 2: Be able to gather artifact from different blah","LO 3: Be able to gather artifact from different operating systems"]}],"references":[{"referenceText":"Reference, First"},{"referenceText":"Reference, Second"},{"referenceText":"Reference, Third"}],"classPolicies":[{"policy":"No eating"},{"policy":"No cheating"}]} ')
        # do stuff
        # return HttpResponseRedirect(reverse('syllabus:dashboard'))
        return HttpResponse("Done")

    def process_json(self, request):
        json = simplejson.loads(request.POST['syllabus_json'])

        # Save Rubric (temporary)
        rubric = None
        try:
            rubric = Rubric.objects.get(pk=1)
        except Exception:
            rubric = Rubric.objects.create(
                rubric_name="Sample Rubric",
                total_rating=100
            )

        # Save College (temporary)
        college = None
        try:
            college = College.objects.get(college_name=json['college'])
        except Exception:
            college = College.objects.create(
                college_name=json['college']
            )

        # Save Department (temporary)
        department = None
        try:
            department = Department.objects.get(
                department_name=json['department'])
        except Exception:
            department = Department.objects.create(
                department_name=json['department'],
                college=college
            )

        # Get Current User
        current_user = get_user_model().objects.get(email=request.user.email)
        syllabus = Syllabus.objects.create(
            user=current_user,
            department=department,
            course_code=json['courseCode'],
            course_description=json['courseDescription'],
            rubric=rubric,
            final_course_output_description=json[
                'finalCourseOutputDescription']
        )

        # Save schedules
        for schedule in json['schedules']:
            ClassSchedule.objects.create(
                syllabus=syllabus,
                days=schedule['days'],
                start_time=datetime.strptime(schedule['startTime'], "%H%M"),
                end_time=datetime.strptime(schedule['endTime'], "%H%M"))

        # Save instructors
        for instructor in json['instructors']:
            Instructor.objects.create(
                syllabus=syllabus,
                instructor_name=instructor['lastName'])

        # Save learning outcomes for later use
        learning_outcomes = []

        for elga in json['elgas']:
            elga_instance = ELGA.objects.create(
                syllabus=syllabus,
                elga_name=elga['elgaName'])

            for learning_outcome in elga['learningOutcomes']:
                learning_outcomes.append(LearningOutcome.objects.create(
                    elga=elga_instance,
                    description=learning_outcome['description']))

        # Save required outputs
        for required_output in json['requiredOutputs']:
            required_output_instance = RequiredOutput.objects.create(
                syllabus=syllabus,
                description=required_output['description'],
                week_due=required_output['weekDue'])

            for learning_outcome in required_output['los']:
                for learning_outcome_instance in learning_outcomes:
                    if learning_outcome_instance.description == learning_outcome:
                        required_output_instance.learning_outcomes.add(
                            learning_outcome_instance)

        # Save other outputs
        for other_requirement in json['otherOutputs']:
            OtherRequirement.objects.create(
                syllabus=syllabus,
                requirement_name=other_requirement['requirementName'])

        # Save grading system,
        for grading_system in json['gradingSystems']:
            GradingSystem.objects.create(
                syllabus=syllabus,
                item_name=grading_system['itemName'],
                percentage=int(grading_system['percentage']))

        # Save learning plans
        for learning_plan in json['learningPlans']:
            saved_learning_plan = LearningPlan.objects.create(
                syllabus=syllabus,
                topic=learning_plan['topic'],
                week_number=int(learning_plan['weekNumber']))

            for learning_outcome in learning_plan['los']:
                for learning_outcome_instance in learning_outcomes:
                    if learning_outcome_instance.description == learning_outcome:
                        saved_learning_plan.learning_outcomes.add(
                            learning_outcome_instance)

            for learning_activity in learning_plan['learningActivities']:
                LearningActivity.objects.create(
                    learning_plan=saved_learning_plan,
                    description=learning_activity['description'])

        # Save references
        for reference in json['references']:
            Reference.objects.create(
                syllabus=syllabus,
                reference_text=reference['referenceText'])

        # Save Class Policies
        for class_policy in json['classPolicies']:
            ClassPolicy.objects.create(
                syllabus=syllabus,
                policy_text=class_policy['policy'])
