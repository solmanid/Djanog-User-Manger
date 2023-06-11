# Third party
# from captcha.fields import CaptchaField
from captcha.fields import CaptchaField
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            # 'id': 'name',
            # 'name': 'name',
            # 'type': 'text',
        }),

        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            # 'id': 'email',
            # 'name': 'email',

        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            # 'id': 'pass',
            # 'name': 'pass',

        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            # 'id': 're_pass',
            # 'name': 're_pass',

        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    captcha = CaptchaField()

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('password dont match')


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            # 'id': 'your_name',
            # 'name': 'your_name',
            # 'type': 'text',
        }),

        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            # 'id': 'your_pass',
            # 'name': 'your_pass',

        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    captcha = CaptchaField()

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',
            # 'id': 'email',
            # 'name': 'email',

        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )
    captcha = CaptchaField()


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            # 'id': 'pass',
            # 'name': 'pass',

        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            # 'id': 're_pass',
            # 'name': 're_pass',

        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    captcha = CaptchaField()
