from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from home_app.models import User
from pharmacy_app.models import Pharmacy


class BaseRegisterForm(forms.ModelForm):
    """Shared behaviour: password + confirmation, unique email, hashing on save."""

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'}),
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-input')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if self._meta.model.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "The two passwords don't match.")
        if p1:
            try:
                password_validation.validate_password(p1)
            except ValidationError as error:
                self.add_error('password1', error)
        return cleaned

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data['password1'])
        if commit:
            account.save()
        return account


class UserRegisterForm(BaseRegisterForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Juan'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Dela Cruz'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '09XX XXX XXXX'}),
        }


class PharmacyRegisterForm(BaseRegisterForm):
    class Meta:
        model = Pharmacy
        fields = ['business_name', 'email', 'contact_number', 'address']
        widgets = {
            'business_name': forms.TextInput(attrs={'placeholder': 'Your pharmacy / drugstore name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'pharmacy@example.com'}),
            'contact_number': forms.TextInput(attrs={'placeholder': '032 XXX XXXX'}),
            'address': forms.TextInput(attrs={'placeholder': 'Street, Barangay, City'}),
        }
