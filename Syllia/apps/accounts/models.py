from django.db import models
from django.contrib.auth import get_user_model


class Faculty(models.Model):
    user = models.OneToOneField(get_user_model())
    # Prevent circular imports?
    department = models.ForeignKey('syllabus.Department')
