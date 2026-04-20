from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect




urlpatterns = [

    path('admin/',admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('dashboard/' , include('apps.dashboard.urls')),
    path('jobs/', include('apps.jobs.urls')),
  

]











