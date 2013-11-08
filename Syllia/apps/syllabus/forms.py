from django.forms import ModelForm
from Syllia.apps.syllabus.models import Feedback


class FeedbackForm(ModelForm):

    class Meta:
        model = Feedback
