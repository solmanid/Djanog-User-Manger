# Third party
# from captcha.fields import CaptchaField

from captcha.fields import CaptchaField
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from accounts.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
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

        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    # type = "checkbox"
    # name = "remember-me"
    # id = "remember-me"
    #
    # class ="agree-term"
    remember_me = forms.CharField(
        label='remember_me',
        widget=forms.CheckboxInput(attrs={
            'name': "remember-me",
            'id': "remember-me",
        })
    )

    captcha = CaptchaField()

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('password dont match')


class LoginForm(forms.Form):
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',

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

        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    captcha = CaptchaField()

    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'name': "remember-me",
            'id': "remember-me",
        }),
        label='remember_me',
        required=False,
    )


class LoginConfirmForm(forms.Form):
    code = forms.CharField(
        label='Code',
        widget=forms.TextInput
            (attrs={
            'class': 'form-control',
            'placeholder': 'Code',
        }),

        validators=[
            validators.MaxLengthValidator(6),
        ]
    )


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email',

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

        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    captcha = CaptchaField()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

        labels = {
            'first_name': 'First Name'
        }


        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name',

            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name',

            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }),

        }


class EditPasswordForm(forms.Form):
    current_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Old password',

        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New password',

        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password',

        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('password dont match')
