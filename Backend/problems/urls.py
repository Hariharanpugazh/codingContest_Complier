from django.urls import path
from . import views

urlpatterns = [
    path('autocontest/',views.userRole,name='save_details'),
    path('get_filtered_problems/', views.get_filtered_problems, name='get_filtered_problems'),
]