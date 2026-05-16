from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        email = request.POST.get('email')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, email=email)
        messages.success(request, 'You have successfully registered. Please log in.')
        return redirect('login')

    return render(request, 'usermodule/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully.')
            return redirect('books.index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'usermodule/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('login')
