from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    # email = forms.EmailField(label='Email Address')
    password = forms.CharField()
