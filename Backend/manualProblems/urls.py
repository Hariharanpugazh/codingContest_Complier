from django.urls import path
from . import views

urlpatterns = [
    path('manualProblems/', views.save_problem, name='save_problem'),
    path('publish/',views.publish_questions,name='harlee')
]