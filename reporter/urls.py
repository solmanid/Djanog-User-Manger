from django.urls import path

from . import views

urlpatterns = [
    path('map', views.ListPoints.as_view(), name='list_points'),
    path('maps', views.LIstPoint.as_view(), name='lists_points'),
    path('edit/<placeID>', views.EditPoint.as_view(), name='edit_points'),
    path('del/<placeID>', views.DeletePoint.as_view(), name='delete_points'),
    path('mine', views.MyPoint.as_view(), name='my_points'),
]
