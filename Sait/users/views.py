from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm

def index(request):
    if request.method == "POST":
        form = UserLoginForm (data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)
            if user: 
                auth.login(request, user)
                return HttpResponseRedirect('lk')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request,'main/login.html', context)

def signin(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:    
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request,'main/signin.html', context)