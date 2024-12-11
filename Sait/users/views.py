from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm

def index(request):
    if request.method == 'POST':
        form = UserLoginForm (data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)
            if user: 
                auth.login(request, user)
                return HttpResponseRedirect('profile')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request,'main/login.html', context)

def signin(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегестрировались!')
            return HttpResponseRedirect('/')

    else:    
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request,'main/signin.html', context)

def profile(request):
    if request.method == "POST":
        form = UserProfileForm(instance = request.user, data=request.POST, files = request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('profile')
        else: 
            print(form.errors)
    else:
        form = UserProfileForm(instance = request.user)
    context = {'form': form}
    return render(request, 'main/profile.html', context) 

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')