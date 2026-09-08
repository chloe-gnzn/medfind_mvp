from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Account created successfully! You can now log in.'
            )
            return redirect('login')  # Transition back to Login Screen
        else:
            messages.error(request, 'Please fix the errors below and try again.')
    else:
        form = RegisterForm()

    return render(request, 'register_app/register.html', {'form': form})
