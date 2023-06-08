# Django
from django import views
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView

# Local Django
from accounts.forms import RegisterForm, LoginForm, ForgotPasswordForm


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

            user = User(username=username, email=email, )
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
            user = authenticate(request, username=username, password=user_pass)
            if user is not None:
                login(request, user)
                messages.success(request, 'You Are Login', 'success')

                return redirect(reverse('home'))
            else:
                form.add_error('username', 'something is wrong')
        context = {
            'form': form
        }
        return render(request, 'accounts/login_page.html', context=context)


class UserLogout(views.View):
    def get(self, request):
        logout(request)
        messages.error(request, 'You Are Logout', 'danger')
        return redirect(reverse('user_login'))


class ForgotPasswordView(LoginRequiredMixin, views.View):
    form_class = ForgotPasswordForm

    def get(self, request):
        form = self.form_class
        context = {
            'form': form
        }
        return render(request, 'accounts/forgot_pass.html', context)

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user: User = User.objects.get(username=username)
            if user is not None:
                # request.session['forgot_username'] = username
                user_pass = form.cleaned_data.get('password')
                user.set_password(user_pass)
                user.save()

                return redirect(reverse('user_login'))

        context = {
            'form': form
        }
        return render(request, 'accounts/forgot_pass.html', context)


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
