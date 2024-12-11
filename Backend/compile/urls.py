from django.urls import path
from . import views, views_auto, views_user
from . import views_contest
from .views_contest import *

urlpatterns = [
    path('compile/',views.compileCode,name='compile'),
    path('submit/',views.compileHidden,name='compile_hidden'),
    path('userinput/', views.userInput, name='user_code'),
    path('manualProblems/', views_auto.save_problem, name='save_problem'),
    path('publish/',views_auto.publish_questions,name='harlee'),
    path('contestdetails/', views_contest.saveDetails, name='save_details'),
    path('userinfo/', views_contest.saveUserInfo, name='save_user_info'),  # New endpoint
    path('api/contests/', get_contests, name='get_contests'),
    path('api/contests/delete/<str:contest_id>/', delete_contest, name='delete_contest'),
    path('api/start_test/', start_test, name='start_test'),
    path('api/finish_test/', finish_test, name='finish_test'),
    path("api/contests/stats/<str:contest_id>/", contest_stats, name="contest_stats"),
    path("api/contests/<str:contest_id>/students/", contest_students, name="contest_students"),
    path('questions/', views_user.fetch_Questions, name='questions'),
    path('saveQuestions/', views_user.fetch_and_save_questions, name= 'saveInFrontend'),
    # path('selected/',views.selectedProblems, name='selected_problems'),
]