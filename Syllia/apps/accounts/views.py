from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import simplejson

from Syllia.apps.accounts.forms import RegisterForm, ProfileForm
from Syllia.apps.accounts.models import Faculty
from Syllia.apps.syllabus.views import get_college_list, get_department_list


class RegisterView(View):
    template_name = "accounts/register.html"
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        jsonData = {
            "collegeList": get_college_list(),
            "departmentList": get_department_list(),
        }

        context = {
            'jsonData': simplejson.dumps(jsonData)
        }

        if request.session.get('register_form'):
            context['form'] = request.session['register_form']
            del request.session['register_form']
        else:
            context['form'] = RegisterForm()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = get_user_model().objects.create_user(
                form.cleaned_data['email'], form.cleaned_data['password'])

            user.name = form.cleaned_data['name']
            user.save()

            faculty = Faculty()
            faculty.department = form.cleaned_data['department']
            faculty.user = user
            faculty.save()

            messages.success(request, 'Successfully created your account')
            return redirect('authtools:login')

        # Not valid, return with errors
        request.session['register_form'] = form
        return redirect('accounts:register')


@csrf_protect
@login_required
def update_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            current_user = get_user_model().objects.get(
                email=request.user.email)

            current_user.name = form.cleaned_data['name']
            current_user.save()

            current_user.faculty.department = form.cleaned_data['department']
            current_user.faculty.save()

            messages.success(request, 'Your profile was updated')
            return redirect('index')

        messages.error(request, 'Something went wrong')
        request.session['profile_form'] = form
        return redirect('index')

    raise Http404


@csrf_protect
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed')
            return redirect('index')

        messages.error(request, 'Something went wrong')
        request.session['change_password_form'] = form
        return redirect('index')

    raise Http404
