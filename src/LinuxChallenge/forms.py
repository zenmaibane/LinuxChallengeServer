from django import forms
from django.contrib.auth.forms import UserCreationForm

from LinuxChallenge.models import User as customUser, Answer


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = customUser


class FlagForm(forms.Form):
    answer = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'FLAG'}))
    q_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        fields = '__all__'


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = {'user', 'question', 'flag', 'scored_time'}

    def is_valid(self):
        # FIXME: Support time limits
        return super(AnswerForm, self).is_valid()

    def clean(self):
        # check the duplicate answer
        return super(AnswerForm, self).clean()


