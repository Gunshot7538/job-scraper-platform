from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('download-csv/', views.download_csv, name='download_csv'),
    path('send-email/', views.send_email, name='send_email'),
    path('contact/', views.contact_view, name='contact_us'),
]