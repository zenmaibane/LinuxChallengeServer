from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=31)
    password = forms.CharField(max_length=127)
    password_again = forms.CharField(max_length=127)


