# Django
from django import views
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import ListView

# Local Django
from accounts.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from accounts.models import User
from utils.email_service import send_email


class CreateUser(views.View):
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register_page.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            email = cd['email']
            password = cd['password']
            user_check = User.objects.filter(username=username).exists()
            user_check_email = User.objects.filter(email=email).exists()

            user = User(username=email, email=email, )
            user.email_active_code = get_random_string(72)

            user.set_password(password)
            user.save()
            messages.success(request, 'create user successfully', 'success')
            return redirect('home')

        messages.error(request, 'some things are wrong', 'danger')
        return render(request, 'accounts/register_page.html', {'form': form})


class UserLogin(views.View):
    form_class = LoginForm

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            messages.info(request, 'You already login', 'info')
            return redirect('home')

        form = self.form_class
        context = {
            'form': form
        }
        return render(request, 'accounts/login_page.html', context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user_pass = form.cleaned_data.get('password')
            # user = authenticate(request, username=username, password=user_pass)
            user = User.objects.get(username=username)
            if user is not None:
                user_check = user.check_password(user_pass)
                if user_check:
                    login(request, user)
                    messages.success(request, 'You Are Login', 'success')
                    return redirect(reverse('home'))
                else:
                    form.add_error('username', 'something is wrong')
            else:
                form.add_error('username', 'something is wrong')
        context = {
            'form': form
        }
        messages.error(request, 'some things wrong', 'danger')
        return render(request, 'accounts/login_page.html', context=context)


class UserLogout(views.View):
    def get(self, request):
        logout(request)
        messages.error(request, 'You Are Logout', 'danger')
        return redirect(reverse('user_login'))


class UserList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list_page.html'
    context_object_name = 'users'

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        user: bool = request.user.is_authenticated
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
                return redirect('user_login')
            user_pass = form.cleaned_data.get('password')
            user.set_password(user_pass)
            user.is_active = True
            user.email_active_code = get_random_string(72)
            user.save()
            return redirect('user_login')
        return render(request, 'accounts/reset_pass.html', {'form': form})
