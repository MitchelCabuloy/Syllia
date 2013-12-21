from django.contrib import admin

from Syllia.apps.syllabus.models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'email', 'fullname')

admin.site.register(Feedback, FeedbackAdmin)
