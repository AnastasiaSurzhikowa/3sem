from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

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
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'proff' }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'proff' }))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'proff' }), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'proff', 'readonly': True }))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'proff', 'readonly': True  }))
    group = forms.ChoiceField(choices=User.options, widget=forms.Select(attrs={'class': 'proff'}))

    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'group', 'image', 'username',)