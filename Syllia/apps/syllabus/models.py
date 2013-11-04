from django.db import models
from django.contrib.auth import get_user_model
from jsonfield import JSONField
# Create your models here.


class Rubric(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model())
    rubric_name = models.CharField(max_length=50)
    json_data = JSONField(default={"pk": 0})
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            super(Rubric, self).save(*args, **kwargs)
            self.json_data = self.json_data.replace(
                '"pk":null', '"pk":%d' % self.id)

        super(Rubric, self).save(*args, **kwargs)

    def json(self):
        return {"pk": self.id, "rubricName": self.rubric_name}

    def __unicode__(self):
        return self.rubric_name


class College(models.Model):
    id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=50)

    def json(self):
        return {"pk": self.id, "collegeName": self.college_name}

    def __unicode__(self):
        return self.college_name


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=50)
    college = models.ForeignKey('syllabus.College')

    def json(self):
        return {"pk": self.id, "departmentName": self.department_name, "college": self.college.id}

    def __unicode__(self):
        return self.department_name


class Syllabus(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model())
    syllabus_name = models.CharField(max_length=50)
    department = models.ForeignKey('syllabus.Department')
    course_code = models.CharField(max_length=7)
    rubric = models.ForeignKey('syllabus.Rubric')
    json_data = JSONField(default={"pk": 0})
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            super(Syllabus, self).save(*args, **kwargs)
            self.json_data = self.json_data.replace(
                '"pk":null', '"pk":%d' % self.id)

        super(Syllabus, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.course_code
