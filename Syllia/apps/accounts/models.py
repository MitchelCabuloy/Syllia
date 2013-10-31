from django.db import models
from django.contrib.auth import get_user_model


class Faculty(models.Model):
    user = models.OneToOneField(get_user_model())
    # Prevent circular imports?
    from Syllia.apps.syllabus.models import Department
    department = models.ForeignKey(Department)
