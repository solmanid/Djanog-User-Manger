# Django Build
from django.urls import path

# Local App
from . import views


urlpatterns = [
    path('', views.show_home, name='home'),
    path('404/', views.show_404, name='show_404'),
]