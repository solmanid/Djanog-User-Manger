from django.urls import path

from . import views

urlpatterns = [
    path('map', views.ListPoint.as_view(), name='lists_points'),
    path('edit/<placeID>', views.EditPoint.as_view(), name='edit_points'),
    path('del/<placeID>', views.DeletePoint.as_view(), name='delete_points'),
]
