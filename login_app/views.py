from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')  # Transition to Home Screen
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'login_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')
