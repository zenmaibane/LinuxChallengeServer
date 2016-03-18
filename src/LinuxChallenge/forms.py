from django import forms
from django.contrib.auth.forms import UserCreationForm
from LinuxChallenge.models import User as custamUser


class SignUpForm(UserCreationForm):

      class Meta(UserCreationForm.Meta):
        model = custamUser




