from django.urls import path
from . import views

urlpatterns = [
    path('contestdetails/',views.saveDetails,name='save_details'),
]