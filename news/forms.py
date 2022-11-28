from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from .models import News, User
from django.core.exceptions import ValidationError


class AddNewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Select a category:'

    class Meta:
        model = News
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'category', 'user']

    def clean_title(self):
        title = self.cleaned_data['title']
        if title[0].isdigit():
            raise ValidationError('The title should not start with a digit!')

        return title


class RegisterUserForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'captcha')


class ChangeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'short_status', 'first_name', 'last_name', 'user_photo')
