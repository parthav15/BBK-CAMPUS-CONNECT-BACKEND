from django.urls import path
from notice import views

urlpatterns = [
    path('get_all_notices/', views.get_all_notices, name='get_all_notices/'),
    path('get_specific_notice/', views.get_specific_notice, name='get_specific_notice'),
]