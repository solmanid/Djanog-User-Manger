# Django Build
from django.urls import path

# Local App
from . import views


urlpatterns = [
    path('register/', views.CreateUser.as_view(), name='user_register'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('logout/', views.UserLogout.as_view(), name='user_logout'),
    path('forgot-pass/', views.ForgotPasswordView.as_view(), name='forgot-pass'),
    path('', views.UserList.as_view(), name='user-list'),
    path('<pk>/remove/', views.UserDel.as_view(), name='user-remove'),
]
