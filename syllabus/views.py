# Create your views here.

from datetime import datetime

from django.contrib.auth import get_user_model
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
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
        if(len(args)):
            current_user = get_user_model().objects.get(
                email=request.user.email)
            # syllabus = current_user.syllabus_set.get(pk=args[0])

            try:
                syllabus = current_user.syllabus_set.get(pk=args[0])
                context = {'jsonString': simplejson.dumps(syllabus.json())}
                return render(request, self.template_name, context)
            except Exception:
                raise Http404

        # If reached here, no arguments. Return empty form
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Get Current User
        current_user = get_user_model().objects.get(email=request.user.email)

        self.process_json(request.POST['syllabus_json'], current_user)

        return HttpResponse(request.POST['syllabus_json'])

    def process_json(self, post_data, current_user):
        json = simplejson.loads(post_data)

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

        # Save syllabus
        syllabus = None
        try:
            syllabus = Syllabus.objects.get(pk=int(json['pk']))
        except Exception:
            syllabus = Syllabus()

        syllabus.user = current_user
        syllabus.department = department
        syllabus.course_code = json['courseCode']
        syllabus.course_description = json['courseDescription']
        syllabus.rubric = rubric
        syllabus.final_course_output_description = json[
            'finalCourseOutputDescription']
        syllabus.save()

        # Save schedules
        for schedule in json['schedules']:
            class_schedule_instance = None
            try:
                class_schedule_instance = ClassSchedule.objects.get(
                    pk=schedule['pk'])
            except Exception:
                class_schedule_instance = ClassSchedule()

            class_schedule_instance.syllabus = syllabus
            class_schedule_instance.days = schedule['days']
            class_schedule_instance.start_time = datetime.strptime(
                schedule['startTime'], "%H%M")
            class_schedule_instance.end_time = datetime.strptime(
                schedule['endTime'], "%H%M")
            class_schedule_instance.save()

        # Save instructors
        for instructor in json['instructors']:
            # If except, not found
            try:
                saved_instructor = Instructor.objects.get(pk=instructor['pk'])
            except Exception:
                saved_instructor = Instructor()

            saved_instructor.syllabus = syllabus
            saved_instructor.instructor_name = instructor['fullName']
            saved_instructor.save()

        # Save learning outcomes for later use
        learning_outcomes = []

        for elga in json['elgas']:

            elga_instance = None
            try:
                elga_instance = ELGA.objects.get(pk=elga['pk'])
            except Exception:
                elga_instance = ELGA()

            elga_instance.syllabus = syllabus
            elga_instance.elga_name = elga['elgaName']
            elga_instance.save()

            for learning_outcome in elga['learningOutcomes']:

                learning_outcome_instance = None
                try:
                    learning_outcome_instance = LearningOutcome.objects.get(
                        pk=learning_outcome['pk'])
                except Exception:
                    learning_outcome_instance = LearningOutcome()

                learning_outcome_instance.elga = elga_instance
                learning_outcome_instance.description = learning_outcome[
                    'description']
                learning_outcome_instance.save()

                learning_outcomes.append(learning_outcome_instance)

        # Save required outputs
        for required_output in json['requiredOutputs']:

            required_output_instance = None
            try:
                required_output_instance = RequiredOutput.objects.get(
                    required_output['pk'])
            except Exception:
                required_output_instance = RequiredOutput()

            required_output_instance.syllabus = syllabus
            required_output_instance.description = required_output[
                'description']
            required_output_instance.week_due = required_output['weekDue']

            # Write to database so we can add stuff to it.
            required_output_instance.save()

            for learning_outcome in required_output['los']:
                for learning_outcome_instance in learning_outcomes:
                    if learning_outcome_instance.description == learning_outcome:
                        required_output_instance.learning_outcomes.add(
                            learning_outcome_instance)

            required_output_instance.save()

        # Save other outputs
        for other_requirement in json['otherOutputs']:

            other_requirement_instance = None
            try:
                other_requirement_instance = OtherRequirement.objects.get(
                    pk=other_requirement['pk'])
            except Exception:
                other_requirement_instance = OtherRequirement()

            other_requirement_instance.syllabus = syllabus
            other_requirement_instance.requirement_name = other_requirement[
                'requirementName']
            other_requirement_instance.save()

        # Save grading system,
        for grading_system in json['gradingSystems']:
            grading_system_instance = None
            try:
                grading_system_instance = GradingSystem.objects.get(
                    pk=grading_system['pk'])
            except Exception:
                grading_system_instance = GradingSystem()

            grading_system_instance.syllabus = syllabus
            grading_system_instance.item_name = grading_system['itemName']
            grading_system_instance.percentage = int(
                grading_system['percentage'])
            grading_system_instance.save()

        # Save learning plans
        for learning_plan in json['learningPlans']:
            learning_plan_instance = None
            try:
                learning_plan_instance = LearningPlan.objects.get(
                    pk=learning_plan['pk'])
            except Exception:
                learning_plan_instance = LearningPlan()

            learning_plan_instance.syllabus = syllabus
            learning_plan_instance.topic = learning_plan['topic']
            learning_plan_instance.week_number = int(
                learning_plan['weekNumber'])

            # Write to database so we can add stuff to it
            learning_plan_instance.save()

            for learning_outcome in learning_plan['los']:
                for learning_outcome_instance in learning_outcomes:
                    if learning_outcome_instance.description == learning_outcome:
                        learning_plan_instance.learning_outcomes.add(
                            learning_outcome_instance)

            learning_plan_instance.save()

            for learning_activity in learning_plan['learningActivities']:

                learning_activity_instance = None
                try:
                    learning_activity_instance = LearningActivity.objects.get(
                        pk=learning_activity['pk'])
                except Exception:
                    learning_activity_instance = LearningActivity()

                learning_activity_instance.learning_plan = learning_plan_instance
                learning_activity_instance.description = learning_activity[
                    'description']
                learning_activity_instance.save()

        # Save references
        for reference in json['references']:

            reference_instance = None
            try:
                reference_instance = Reference.objects.get(pk=reference['pk'])
            except Exception:
                reference_instance = Reference()

            reference_instance.syllabus = syllabus
            reference_instance.reference_text = reference['referenceText']
            reference_instance.save()

        # Save Class Policies
        for class_policy in json['classPolicies']:

            class_policy_instance = None
            try:
                class_policy_instance = ClassPolicy.objects.get(
                    pk=class_policy['pk'])
            except Exception:
                class_policy_instance = ClassPolicy()

            class_policy_instance.syllabus = syllabus
            class_policy_instance.policy_text = class_policy['policy']
            class_policy_instance.save()
