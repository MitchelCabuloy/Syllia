from django.db import models
from django.contrib.auth import get_user_model

short_length = 10
medium_length = 50
long_length = 100
very_long_length = 400


# Create your models here.

def clear_database():
    Rubric.objects.all().delete()
    College.objects.all().delete()
    Department.objects.all().delete()
    Syllabus.objects.all().delete()
    ClassSchedule.objects.all().delete()
    Room.objects.all().delete()
    Instructor.objects.all().delete()
    ELGA.objects.all().delete()
    LearningOutcome.objects.all().delete()
    RequiredOutput.objects.all().delete()
    Criteria.objects.all().delete()
    OtherRequirement.objects.all().delete()
    GradingSystem.objects.all().delete()
    LearningPlan.objects.all().delete()
    LearningActivity.objects.all().delete()
    Reference.objects.all().delete()
    ClassPolicy.objects.all().delete()


class Rubric(models.Model):
    id = models.AutoField(primary_key=True)
    rubric_name = models.CharField(max_length=medium_length)
    total_rating = models.IntegerField()


class College(models.Model):
    id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=medium_length)


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=medium_length)
    college = models.ForeignKey(College)


class Syllabus(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model())
    department = models.ForeignKey(Department)
    course_code = models.CharField(max_length=7)
    course_description = models.CharField(max_length=very_long_length)
    rubric = models.ForeignKey(Rubric)
    final_course_output_description = models.CharField(
        max_length=very_long_length)

    def json(self):
        return {
            "pk": self.id,
            "college": str(self.department.college.college_name),
            "department": str(self.department.department_name),
            "courseCode": str(self.course_code),
            "courseName": str(self.course_code),
            "courseDescription": str(self.course_description),
            "schedules": [s.json() for s in self.classschedule_set.all()],
            "instructors": [instructor.json() for instructor in self.instructor_set.all()],
            "elgas": [elga.json() for elga in self.elga_set.all()],
            "finalCourseOutputDescription": str(self.final_course_output_description),
            "requiredOutputs": [required_output.json() for required_output in self.requiredoutput_set.all()],
            "otherOutputs": [other_output.json() for other_output in self.otherrequirement_set.all()],
            "gradingSystems": [grading_system.json() for grading_system in self.gradingsystem_set.all()],
            "learningPlans": [learning_plan.json() for learning_plan in self.learningplan_set.all()],
            "references": [reference.json() for reference in self.reference_set.all()],
            "classPolicies": [class_policy.json() for class_policy in self.classpolicy_set.all()]
        }


class ClassSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    syllabus = models.ForeignKey(Syllabus)
    days = models.CharField(max_length=5)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def json(self):
        return {
            "pk": self.id,
            "days": str(self.days),
            "startTime": str(self.start_time.strftime("%H%M")),
            "endTime": str(self.end_time.strftime("%H%M"))
        }


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    syllabus = models.ForeignKey(Syllabus)
    room_name = models.CharField(max_length=short_length)


class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    syllabus = models.ForeignKey(Syllabus)
    instructor_name = models.CharField(max_length=medium_length)

    def json(self):
        return {
            "pk": self.id,
            "firstName": "",
            "lastName": str(self.instructor_name)
        }


class ELGA(models.Model):
    id = models.AutoField(primary_key=True)
    syllabus = models.ForeignKey(Syllabus)
    elga_name = models.CharField(max_length=medium_length)

    def json(self):
        return {
            "pk": self.id,
            "elgaName": str(self.elga_name),
            "learningOutcomes": [lo.json() for lo in self.learningoutcome_set.all()]
        }


class LearningOutcome(models.Model):
    id = models.AutoField(primary_key=True)
    elga = models.ForeignKey(ELGA)
    description = models.CharField(max_length=long_length)

    def json(self):
        return {
            "pk": self.id,
            "description": str(self.description)
        }


class RequiredOutput(models.Model):
    id = models.AutoField(primary_key=True)
    syllabus = models.ForeignKey(Syllabus)
    description = models.CharField(max_length=long_length)
    week_due = models.IntegerField()
    learning_outcomes = models.ManyToManyField(LearningOutcome)

    def json(self):
        return {
            "pk": self.id,
            "description": str(self.description),
            "weekDue": str(self.week_due),
            "los": [str(lo.description) for lo in self.learning_outcomes.all()]
        }


class Criteria(models.Model):
    id = models.AutoField(primary_key=True)
    rubric = models.ForeignKey(Rubric)
    criteria_name = models.CharField(max_length=medium_length)
    exemplary_description = models.CharField(max_length=long_length)
    satisfactory_description = models.CharField(max_length=long_length)
    developing_description = models.CharField(max_length=long_length)
    beginning_description = models.CharField(max_length=long_length)
    rating = models.IntegerField()


class OtherRequirement(models.Model):
    id = models.AutoField(primary_key=True)
    syllabus = models.ForeignKey(Syllabus)
    requirement_name = models.CharField(max_length=medium_length)

    def json(self):
        return {
            "pk": self.id,
            "requirementName": str(self.requirement_name)
        }


class GradingSystem(models.Model):
    id = models.AutoField(primary_key=True)
    syllabus = models.ForeignKey(Syllabus)
    item_name = models.CharField(max_length=medium_length)
    percentage = models.IntegerField()

    def json(self):
        return {
            "pk": self.id,
            "itemName": str(self.item_name),
            "percentage": str(self.percentage)
        }


class LearningPlan(models.Model):
    id = models.AutoField(primary_key=True)
    syllabus = models.ForeignKey(Syllabus)
    topic = models.CharField(max_length=medium_length)
    week_number = models.IntegerField()
    learning_outcomes = models.ManyToManyField(LearningOutcome)

    def json(self):
        return {
            "pk": self.id,
            "topic": str(self.topic),
            "weekNumber": str(self.week_number),
            "learningActivities": [learning_activity.json() for learning_activity in self.learningactivity_set.all()],
            "los": [str(lo.description) for lo in self.learning_outcomes.all()]
        }


class LearningActivity(models.Model):
    id = models.AutoField(primary_key=True)
    learning_plan = models.ForeignKey(LearningPlan)
    description = models.CharField(max_length=medium_length)

    def json(self):
        return {
            "pk": self.id,
            "description": str(self.description)
        }


class Reference(models.Model):
    id = models.AutoField(primary_key=True)
    syllabus = models.ForeignKey(Syllabus)
    reference_text = models.CharField(max_length=very_long_length)

    def json(self):
        return {
            "pk": self.id,
            "referenceText": str(self.reference_text)
        }


class ClassPolicy(models.Model):
    id = models.AutoField(primary_key=True)
    syllabus = models.ForeignKey(Syllabus)
    policy_text = models.CharField(max_length=very_long_length)

    def json(self):
        return {
            "pk": self.id,
            "policy": str(self.policy_text)
        }
