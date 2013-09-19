# Create your views here.

from django.contrib.auth import get_user_model
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils import simplejson
from syllabus.models import *
from datetime import datetime


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
        self.processJSON(request)
        # parsed_json = simplejson.loads('{"college":"College of Computer Studies","department":"Computer Technology","courseCode":"LBYFORE","courseName":"LBYFORE","courseDescription":"LBYFORE is a course that ahds-on laboratory component of FORENSC.","schedules":[{"days":"S","startTime":"1440","endTime":"1740"},{"days":"TH","startTime":"1300","endTime":"1600"}],"instructors":[{"firstName":"Cu","lastName":"Gregory"},{"firstName":"Pantola","lastName":"Alexi"}],"elgas":[{"elgaName":"Effective Communicator","learningOutcomes":[{"description":"LO 1: Be able to discuss different digital blah."}]},{"elgaName":"Critical/creative thinker","learningOutcomes":[{"description":"LO 2: Be able to gather artifact from different blah"},{"description":"LO 3: Be able to gather artifact from different operating systems"}]}],"finalCourseOutputDescription":"Final course output description here","requiredOutputs":[{"description":"Forensic Platform Preparation Report","weekDue":"4","los":["LO 1: Be able to discuss different digital blah."]},{"description":"Windows System and Artifacts Report","weekDue":"5","los":["LO 2: Be able to gather artifact from different blah","LO 3: Be able to gather artifact from different operating systems"]}],"otherOutputs":[{"requirementName":"Laboratory Exam"},{"requirementName":"Group Project"}],"gradingSystems":[{"itemName":"Laboratory Report Average","percentage":"60"},{"itemName":"Group Project","percentage":"20"},{"itemName":"Laboratory Exam","percentage":"20"}],"totalGradingSystem":100,"learningPlans":[{"topic":"Introduction / Orientation","weekNumber":"1","learningActivities":[{"description":"Course introduction"},{"description":"Classroom policies discussion"}],"los":[]},{"topic":"1.0 Forensic Platform Preparation","weekNumber":"3","learningActivities":[{"description":"Hands-on"}],"los":["LO 1: Be able to discuss different digital blah."]},{"topic":"2.0 Windows Systems and Artifacts","weekNumber":"4","learningActivities":[{"description":"Hands-on"}],"los":["LO 2: Be able to gather artifact from different blah","LO 3: Be able to gather artifact from different operating systems"]}],"references":[{"referenceText":"Reference, First"},{"referenceText":"Reference, Second"},{"referenceText":"Reference, Third"}],"classPolicies":[{"policy":"No eating"},{"policy":"No cheating"}]} ')
        # do stuff
        # return HttpResponseRedirect(reverse('syllabus:dashboard'))
        return HttpResponse("Done")

    def processJSON(self, request):
        json = simplejson.loads(request.POST['syllabus_json'])

        # Save Rubric
        rubric = None
        try:
            rubric = Rubric.objects.get(pk=1)
        except Exception, e:
            rubric = Rubric.objects.create(
                rubric_name="Sample Rubric",
                total_rating=100
            )

        # Save College (temporary)
        college = None
        try:
            college = College.objects.get(college_name=json['college'])
        except Exception, e:
            college = College.objects.create(
                college_name=json['college']
            )

        # Save Department (temporary)
        department = None
        try:
            department = Department.objects.get(
                department_name=json['department'])
        except Exception, e:
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
            rubric=rubric
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
        learningOutcomes = []

        for elga in json['elgas']:
            saved_elga = ELGA.objects.create(
                syllabus=syllabus,
                elga_name=elga['elgaName'])

            for lo in elga['learningOutcomes']:
                learningOutcomes.append(LearningOutcome.objects.create(
                    elga=saved_elga,
                    description=lo['description']))

        # Save final course output
        final_course_output = FinalCourseOutput.objects.create(
            syllabus=syllabus,
            description=json['finalCourseOutputDescription'])

        # Save required outputs
        for requiredOutput in json['requiredOutputs']:
            ro = RequiredOutput.objects.create(
                final_course_output=final_course_output,
                description=requiredOutput['description'],
                week_due=requiredOutput['weekDue'])

            for lo in requiredOutput['los']:
                for learningOutcome in learningOutcomes:
                    if learningOutcome.description == lo:
                        ro.learning_outcomes.add(learningOutcome)

        # Save other outputs
        for otherRequirement in json['otherOutputs']:
            OtherRequirement.objects.create(
                syllabus=syllabus,
                requirement_name=otherRequirement['requirementName'])

        # Save grading system,
        for gradingSystem in json['gradingSystems']:
            GradingSystem.objects.create(
                syllabus=syllabus,
                item_name=gradingSystem['itemName'],
                percentage=int(gradingSystem['percentage']))

        # Save learning plans
        for learningPlan in json['learningPlans']:
            saved_learning_plan = LearningPlan.objects.create(
                syllabus=syllabus,
                topic=learningPlan['topic'],
                week_number=int(learningPlan['weekNumber']))

            for lo in learningPlan['los']:
                for learningOutcome in learningOutcomes:
                    if learningOutcome.description == lo:
                        saved_learning_plan.learning_outcomes.add(
                            learningOutcome)

            for learningActivity in learningPlan['learningActivities']:
                LearningActivity.objects.create(
                    learning_plan=saved_learning_plan,
                    description=learningActivity['description'])

        # Save references
        for reference in json['references']:
            Reference.objects.create(
                syllabus=syllabus,
                reference_text=reference['referenceText'])

        # Save Class Policies
        for cp in json['classPolicies']:
            ClassPolicy.objects.create(
                syllabus=syllabus,
                policy_text=cp['policy'])
