from django.urls import path
from .views import *

urlpatterns = [
    path("login/", student_login, name="student_login"),
    path("signup/", student_signup, name="student_signup"),
    path("profile/", student_profile, name="student_profile"),
    path("", get_students, name="get_students"),
    path("tests", get_tests_for_student, name="get_open_tests"),
    # path("tests/", student_tests, name="student_tests"),

]
