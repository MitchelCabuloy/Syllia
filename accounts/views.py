from django.views.generic.base import View
from django.shortcuts import render


class ProfileView(View):
    template_name = "accounts/profile.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
