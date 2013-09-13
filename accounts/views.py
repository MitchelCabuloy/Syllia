from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.shortcuts import render
from django.core.urlresolvers import reverse
from accounts.forms import LoginForm
from django.contrib.auth import authenticate, login


class LoginView(View):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('syllabus:index'))

        # If reached here, something went wrong. Redisplay form
        return render(request, self.template_name, {'form': form})
