# urls.py
from django.urls import path
from . import views
from .views import get_contests
from .views import delete_contest

urlpatterns = [
    path('contestdetails/', views.saveDetails, name='save_details'),
    path('userinfo/', views.saveUserInfo, name='save_user_info'),  # New endpoint
    path('api/contests/', get_contests, name='get_contests'),
    path('api/contests/delete/<str:contest_id>/', delete_contest, name='delete_contest'),
    path('finish/', views.finish_contest, name='publish_contest') # New endpoint
]