from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-text' }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-text' }))

    class Meta:
        model = User
        fields = ('username', 'password')

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-text' }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-text' }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-text' }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-text' }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-text' }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-text' }))    

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')