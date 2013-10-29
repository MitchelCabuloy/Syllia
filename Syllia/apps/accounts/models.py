from django.db import models
from django.contrib.auth import get_user_model
from Syllia.apps.syllabus.models import Department


class Faculty(models.Model):
    user = models.OneToOneField(get_user_model())
    department = models.ForeignKey(Department)
