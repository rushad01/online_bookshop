from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label='Password Confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        # for disabling long default help text


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']


class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(
        label='Password Confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
