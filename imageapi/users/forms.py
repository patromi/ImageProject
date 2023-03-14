from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ImageUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = ImageUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = ImageUser
        fields = ("email",)
