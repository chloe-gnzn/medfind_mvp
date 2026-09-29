from django.contrib import messages
from django.shortcuts import render, redirect

from medfind_project.session_auth import (
    ROLE_HOME, SESSION_ID, SESSION_ROLE,
    get_account, login_account, logout_account,
)

from .forms import LoginForm
from .utils import log_activity


def login_view(request):
    if get_account(request):
        return redirect(ROLE_HOME[request.session[SESSION_ROLE]])

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            account = form.account
            login_account(request, role, account)
            log_activity(role, account.pk, 'login', f'{account.email} logged in.')
            messages.success(request, f'Welcome back, {account.display_name}!')
            return redirect(ROLE_HOME[role])  # Transition to the role's home screen
    else:
        form = LoginForm()

    return render(request, 'login_app/login.html', {'form': form})


def logout_view(request):
    role = request.session.get(SESSION_ROLE)
    account_id = request.session.get(SESSION_ID)
    if role and account_id:
        log_activity(role, account_id, 'logout', 'Logged out.')
    logout_account(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')
