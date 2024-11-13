from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.fetch_Questions, name='questions'),
    path('saveQuestions/', views.fetch_and_save_questions, name= 'saveInFrontend'),
]
