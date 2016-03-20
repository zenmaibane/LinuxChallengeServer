from django.contrib.auth.forms import UserCreationForm
from LinuxChallenge.models import User as customUser


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = customUser


