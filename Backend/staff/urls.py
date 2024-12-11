from django.urls import path
from .views import *

urlpatterns = [
    path("login/", staff_login, name="staff_login"),
    path("signup/", staff_signup, name="staff_signup"),
    # path("profile/", staff_profile, name="staff_profile"),
    # path("get_students/", get_students, name="get_students"),

]
