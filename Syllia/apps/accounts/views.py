from django.contrib.auth import get_user_model
from django.views.generic.base import View
from django.shortcuts import render, redirect

from Syllia.apps.accounts.forms import RegisterForm, ProfileForm


class ProfileView(View):
    template_name = "accounts/profile.html"
    form_class = ProfileForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST)

        if form.is_valid():
            current_user = get_user_model().objects.get(
                email=request.user.email)

            current_user.name = form.cleaned_data['name']
            current_user.save()

            current_user.faculty.department = form.cleaned_data['department']
            current_user.faculty.save()

            return redirect('index')

        return redirect('index')


class RegisterView(View):
    template_name = "accounts/register.html"
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = get_user_model().objects.create_user(
                form.cleaned_data['email'], form.cleaned_data['password'])

            user.name = form.cleaned_data['name']
            user.save()

            return redirect('authtools:login')

        return render(request, self.template_name, {'form': form})
