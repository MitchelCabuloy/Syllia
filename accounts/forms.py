from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email Address')
    name = forms.CharField()
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

        if not "@delasalle.ph" in email:
            raise forms.ValidationError(
                "You need to use a @delasalle.ph email address to sign up for this service.")

        return email
