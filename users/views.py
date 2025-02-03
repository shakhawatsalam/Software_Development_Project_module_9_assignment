from django.shortcuts import render, redirect
from users.forms import RegistrationForm, LoginForm
from django.contrib.auth  import login, logout
from django.contrib import  messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse


# SIGN-UP / REGISTER
def sign_up(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            messages.success(request, 'A Confirmation mail sent. Please Check your Email')
            return redirect('sign-in')
    return render(request, 'registration/register.html', {"form" :  form})

# ACTIVATE USER
def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if  default_token_generator.check_token(user,  token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        
        else:
            return HttpResponse('Invalid Id or Token')
    except User.DoesNotExist:
        return HttpResponse('User not found')
# SIGN-IN / LOG IN
def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {"form" :  form})


# SIGN-OUT / LOG OUT
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')