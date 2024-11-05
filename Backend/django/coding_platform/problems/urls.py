from django.urls import path
from . import views

urlpatterns = [
    path('autocontest/',views.userRole,name='save_details'),
]