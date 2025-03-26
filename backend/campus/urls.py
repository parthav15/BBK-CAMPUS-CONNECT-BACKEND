from django.urls import path
from campus import views

urlpatterns = [
    path('campus_list/', views.get_all_campuses, name="campus_list"),
    path('create_incident/', views.create_incident, name="create_incident"),
    path('get_incidents/', views.get_incidents, name="get_incidents"),
    path('get_specific_incident/', views.get_specific_incident, name='get_specific_incident'),
]