from django import forms
from Syllia.apps.syllabus.models import Department, College


class ProfileForm(forms.Form):
    name = forms.CharField()
    college = forms.ModelChoiceField(queryset=College.objects.all())
    department = forms.ModelChoiceField(queryset=Department.objects.all())


class RegisterForm(ProfileForm):
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError("The passwords do not match.")

        return password

    def clean_email(self):
        email = self.cleaned_data['email']

        if not "@dlsu.edu.ph" in email and not "@delasalle.ph" in email:
            raise forms.ValidationError(
                "You need to use a valid @dlu.edu.ph or @delasalle.ph email address to sign up for this service.")

        return email
