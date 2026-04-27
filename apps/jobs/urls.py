from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('clear-resume/', views.clear_resume, name='clear_resume'),
    path('submit-support-query/', views.submit_support_query, name='submit_support_query'),
]