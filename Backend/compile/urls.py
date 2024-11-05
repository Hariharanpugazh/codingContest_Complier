<<<<<<< HEAD:Backend/django/coding_platform/compile/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('compile/',views.compileCode,name='compile'),
    path('submit/',views.compileHidden,name='compile_hidden'),
    path('userinput/', views.userInput, name='user_code'),
    # path('selected/',views.selectedProblems, name='selected_problems'),
=======
from django.urls import path
from . import views

urlpatterns = [
    path('compile/',views.compileCode,name='compile'),
    path('submit/',views.compileHidden,name='compile_hidden'),
    path('userinput/', views.userInput, name='user_code'),
    # path('selected/',views.selectedProblems, name='selected_problems'),
>>>>>>> 0ff863994d41a0e628cdce9ffb38d65a4e9ce576:Backend/compile/urls.py
]