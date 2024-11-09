from django.urls import path
from . import views

urlpatterns = [
    path('fetchAutoSelectProblems/', views.fetch_AutoSelect_problems, name='fetch_problems'),
    path('fetchFileUploadProblems/', views.fetch_FileUpload_problems, name='fetch_all_file_upload_problems'),
    path('fetchManualUploadProblems/', views.fetch_ManualUpload_problems,name = 'fetchManualUploadProblems'),
    path('questions/', views.fetch_Questions,name='questions'),
    path('getQuestionById/', views.get_question_by_id, name='get_question_by_id'),
]
