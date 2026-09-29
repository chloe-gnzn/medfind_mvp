from django import forms

from medfind_project.session_auth import get_account_model


class LoginForm(forms.Form):
    """Email + password login for any of the three ERD account types."""

    ROLE_CHOICES = [
        ('user', 'User'),
        ('pharmacy', 'Pharmacy'),
        ('admin', 'Admin'),
    ]

    role = forms.ChoiceField(
        label='Log in as',
        choices=ROLE_CHOICES,
        initial='user',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'you@example.com',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
        }),
    )

    account = None  # filled in by clean() when the credentials are valid

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get('role')
        email = cleaned.get('email')
        password = cleaned.get('password')

        if role and email and password:
            account = get_account_model(role).objects.filter(email__iexact=email.strip()).first()
            if account is None or not account.check_password(password):
                raise forms.ValidationError(
                    'Invalid email or password for the selected account type.'
                )
            if role == 'pharmacy' and not account.is_active:
                raise forms.ValidationError('This pharmacy account has been deactivated.')
            self.account = account
        return cleaned
