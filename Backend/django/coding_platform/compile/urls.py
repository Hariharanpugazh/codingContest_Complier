from django.urls import path
from . import views

urlpatterns = [
    path('compile/',views.compileCode,name='compile'),
    path('submit/',views.compileHidden,name='compile_hidden'),
    path('userinput/', views.userInput, name='user_code'),
    path('selected/',views.selectedProblems, name='selected_problems'),
]