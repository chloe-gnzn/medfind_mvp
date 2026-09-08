from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Registration form for MedFind users.

    Extends Django's built-in UserCreationForm (which already validates:
      - password1 / password2 match
      - password strength rules from AUTH_PASSWORD_VALIDATORS
      - username uniqueness
    and adds an email field with its own uniqueness check.
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'you@example.com',
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Choose a username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Create a password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm your password',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
