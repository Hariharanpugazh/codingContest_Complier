# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('contestdetails/', views.saveDetails, name='save_details'),
    path('userinfo/', views.saveUserInfo, name='save_user_info'),  # New endpoint
]
