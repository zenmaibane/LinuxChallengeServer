from django.contrib.auth.forms import UserCreationForm
from LinuxChallenge.models import User as customUser, Question
from django import forms


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = customUser


class FlagForm(forms.Form):
    answer = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'FLAG'}))
    q_id = forms.IntegerField(widget=forms.HiddenInput)

