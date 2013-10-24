from django.db import models
from django.contrib.auth import get_user_model
from jsonfield import JSONField
# Create your models here.


class Rubric(models.Model):
    id = models.AutoField(primary_key=True)
    rubric_name = models.CharField(max_length=50)
    total_rating = models.IntegerField()

    def __unicode__(self):
        return self.rubric_name


class College(models.Model):
    id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.college_name


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=50)
    college = models.ForeignKey(College)

    def __unicode__(self):
        return self.department_name


class Syllabus(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model())
    department = models.ForeignKey(Department)
    course_code = models.CharField(max_length=7)
    rubric = models.ForeignKey(Rubric)
    json_data = JSONField(default={"pk": 0})

    def save(self, *args, **kwargs):
        if self.id == None:
            super(Syllabus, self).save(*args, **kwargs)
            self.json_data = self.json_data.replace(
                '"pk":null', '"pk":%d' % self.id)

        super(Syllabus, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.course_code
