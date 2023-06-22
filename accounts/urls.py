# Django Build
from django.urls import path

# Local App
from . import views


urlpatterns = [
    path('register/', views.CreateUser.as_view(), name='user_register'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('login-c/', views.UserLoginConfirm.as_view(), name='user_login_confirm'),
    path('logout/', views.UserLogout.as_view(), name='user_logout'),
    path('edit/', views.EditUser.as_view(), name='edit_user'),
    path('edit/pass/', views.EditPassword.as_view(), name='edit_user_pass'),
    path('', views.UserList.as_view(), name='user-list'),
    path('<pk>/remove/', views.UserDel.as_view(), name='user-remove'),
    path('forgot-pass/', views.ForgotPasswordView.as_view(), name='forgot-pass'),
    path('reset-pass/<active_code>', views.ResetPasswordView.as_view(), name='reset-pass'),
]

