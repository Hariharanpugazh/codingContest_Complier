# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('contestdetails/', views.saveDetails, name='save_details'),
    path('userinfo/', views.saveUserInfo, name='save_user_info'), 
    path('publish/', views.publish_contest, name='publish_contest') # New endpoint
]