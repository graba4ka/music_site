from typing import Any
from django import forms
from django.contrib.auth.forms import (
    BaseUserCreationForm,
    UserCreationForm,
    AuthenticationForm,
)
from django.contrib.auth import get_user_model
from django.forms import CharField, ChoiceField, DateField, Form, ValidationError, ModelForm
from django.forms.widgets import DateInput

User = get_user_model()






class SignupForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "music_style"
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError("User with this email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.name = self.cleaned_data["name"]
        user.music_style = self.cleaned_data["music_style"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm): ...



class UploadSongForm(forms.Form):
    title = forms.CharField(max_length=100)
    category = forms.CharField(max_length=100)
    audio_file = forms.FileField()
