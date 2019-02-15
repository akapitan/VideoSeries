from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserLoginForm, UserRegisterFrom
from django.contrib.auth.hashers import make_password

def loginView(request):
    next = request.GET.get('next')
    print(next)
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form':form,
    }
    return render(request, 'accounts/login.html', context)

def registerView(request):
    form = UserRegisterFrom(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('/')

    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)

def logoutView(request):
    logout(request)
    redirect('/')