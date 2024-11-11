from django.urls import path
from . import views

urlpatterns = [
    path('manualProblems/', views.save_problem, name='save_problem'),
    # path('manualProblems/delete', views.delete_problem_data, name = 'delete'),
]