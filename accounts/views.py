# Python
import datetime
import random

# Django build-in
from django import views
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import ListView

# Local Django
from accounts.forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    LoginConfirmForm,
    ProfileForm,
    EditPasswordForm
)
from accounts.models import User, OtpCode
from utils.email_service import send_email


# Third Party


class CreateUser(views.View):
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register_page.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # username = cd['username']
            email = cd['email']
            password = cd['password']
            user_check = User.objects.filter(username=email).exists()  # check user is created before or no
            if user_check is True:
                messages.error(request, 'This user already exist', 'danger')
                return render(request, 'accounts/register_page.html', {'form': form})
            # Create user happened
            user = User(username=User.objects.normalize_email(email), email=email, )
            user.email_active_code = get_random_string(72)

            user.set_password(password)
            user.save()
            messages.success(request, 'create user successfully', 'success')
            return redirect('user_login')

        messages.error(request, 'some things are wrong', 'danger')
        return render(request, 'accounts/register_page.html', {'form': form})


class UserLogin(views.View):
    form_class = LoginForm

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            messages.info(request, 'You already login', 'info')
            return redirect('edit_user')

        form = self.form_class

        context = {
            'form': form
        }
        return render(request, 'accounts/login_page.html', context=context)

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_pass = form.cleaned_data.get('password')
            user = User.objects.filter(username=User.objects.normalize_email(email)).first()  # check user exists or not
            if user is not None:
                user_check = user.check_password(user_pass)
                if user_check:  # check pass
                    otp = OtpCode.objects.create(email=user.email, code=random.randint(1000, 9999))
                    otp_code = otp.code
                    login(request, user)
                    request.session['otp_code'] = otp_code  # we save it because want to send it for 2verifying
                    send_email(
                        subject='Login Confirm',
                        to=user.email,
                        context={'otp_code': otp_code},
                        template_name='emails/login_confirm.html')

                    messages.success(request, f'We send email to {user.email}', 'success')

                    # todo: login automatically

                    remember_me = request.POST.get('remember_me', False)
                    if remember_me:
                        request.session.set_expiry(12000)  # Set a longer expiry
                    else:
                        request.session.set_expiry(12000)
                    return redirect(reverse('user_login_confirm'))
                else:
                    form.add_error('email', 'something is wrong')
            else:
                messages.error(request, 'User dos not exist', 'danger')
                return render(request, 'accounts/login_page.html', {'form': form})

        messages.error(request, 'User dos not exist', 'danger')

        context = {
            'form': form
        }
        messages.error(request, 'some things wrong', 'danger')
        return render(request, 'accounts/login_page.html', context=context)


class UserLoginConfirm(views.View):
    form_class = LoginConfirmForm

    def get(self, request):
        form = self.form_class
        return render(request, "accounts/login_confirm.html", {'form': form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            # this session defined at UserLogin view
            otp_session = request.session.get('otp_code')

            otp_form = int(form.cleaned_data.get('code'))

            if otp_form == otp_session:
                otp_user = OtpCode.objects.get(code__exact=otp_form)

                if otp_user is not None:
                    # otp code before 2 min will be deleted
                    otp_date = otp_user.created.minute + 2
                    time_now = datetime.datetime.now().minute
                    time_end: bool = otp_date > time_now

                    if time_end is True:
                        user = User.objects.filter(email__iexact=otp_user.email).first()
                        login(request, user)
                        messages.success(request, 'You are login', 'success')
                        otp_user.delete()
                        return redirect('edit_user')

                    else:
                        # after any login user otp will be deleted
                        otp_user.delete()
                        messages.error(request, 'Code time is dead ', 'danger')
                        return render(request, 'accounts/login_confirm.html', {'form': form})

                messages.error(request, 'code is wrong', 'danger')
                return render(request, 'accounts/login_confirm.html', {'form': form})

            messages.error(request, 'code is wrong', 'danger')
            return render(request, 'accounts/login_confirm.html', {'form': form})

        return render(request, 'accounts/login_confirm.html', {'form': form})


class UserLogout(views.View):
    def get(self, request):
        logout(request)
        messages.error(request, 'You Are Logout', 'danger')
        return redirect(reverse('user_login'))


class UserList(LoginRequiredMixin, ListView):
    """
    a list of users
    only admin can see
    """
    model = User
    template_name = 'accounts/user_list_page.html'
    context_object_name = 'users'

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        user: bool = request.user.is_authenticated
        if request.user.is_superuser is not True:
            messages.error(request, '404', 'danger')
            return redirect('show_404')
        if user is not True:
            messages.error(request, '404', 'danger')
            return redirect('show_404')

        return super(UserList, self).dispatch(request, *args, **kwargs)


class UserDel(views.View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        user.delete()
        messages.success(request, 'Deleted', 'success')
        return redirect('user-list')


class ForgotPasswordView(views.View):
    form_class = ForgotPasswordForm

    def get(self, request):
        form = self.form_class
        context = {
            'form': form
        }
        return render(request, 'accounts/forgot_pass.html', context)

    def post(self, request: HttpRequest):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email(
                    subject='Account Recovery',
                    to=user.email,
                    context={'user': user},
                    template_name='emails/forgot_account.html')
                messages.success(request, f'We send email to {user_email}', 'success')
                return redirect(reverse('user_login'))

        context = {
            'form': form
        }
        return render(request, 'accounts/forgot_pass.html', context)


class ResetPasswordView(views.View):
    form_class = ResetPasswordForm

    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect('user_login')
        form = self.form_class
        return render(request, 'accounts/reset_pass.html', {'form': form, 'user': user})

    def post(self, request: HttpRequest, active_code):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.filter(email_active_code__iexact=active_code).first()
            if user is None:
                messages.error(request, 'some thing wrong', 'danger')
                return redirect('user_login')

            user_pass = form.cleaned_data.get('password')
            user.set_password(user_pass)
            user.is_active = True
            user.email_active_code = get_random_string(72)
            user.save()
            messages.success(request, 'Password changed', 'success')
            return redirect('user_login')

        messages.error(request, 'some thing wrong', 'danger')
        return render(request, 'accounts/reset_pass.html', {'form': form})


class EditUser(LoginRequiredMixin, views.View):
    form_class = ProfileForm

    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        form = self.form_class(instance=current_user)

        return render(request, 'accounts/edit_user.html', {'form': form, 'user': current_user})

    def post(self, request: HttpRequest):
        current_user: User = User.objects.filter(id=request.user.id).first()
        form = self.form_class(request.POST, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Updated successfully', 'success')
            return render(request, 'accounts/edit_user.html', {'form': form, 'user': current_user})

        messages.error(request, 'Form is not valid', 'danger')
        return render(request, 'accounts/edit_user.html', {'form': form, 'user': current_user})


class EditPassword(LoginRequiredMixin, views.View):
    form_class = EditPasswordForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/edit_profile_pass.html', {'form_pass': form})

    def post(self, request):
        current_user: User = User.objects.filter(id=request.user.id).first()
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if current_user.check_password(cd.get('current_password')):
                current_user.set_password(cd.get('confirm_password'))
                current_user.save()

                messages.success(request, 'Updated successfully', 'success')
                return redirect('user_login')

        messages.error(request, 'Form is not valid', 'danger')
        return render(request, 'accounts/edit_profile_pass.html', {'form_pass': form, 'user': current_user})
