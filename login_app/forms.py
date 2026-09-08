from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """AuthenticationForm with the shared form-input styling applied."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Enter your username',
            'autofocus': True,
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Enter your password',
        })
