from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect




def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

urlpatterns = [

    path('admin/',admin.site.urls),
    path('', home_redirect, name='home'),
    path('accounts/' , include('apps.accounts.urls')),
    path('dashboard/' , include('apps.dashboard.urls')),
    path('jobs/', include('apps.jobs.urls')),
  

]











# from django.contrib import admin
# from django.urls import path, include
# from django.shortcuts import redirect


# def home_redirect(request):
#     if request.user.is_authenticated:
#         return redirect('dashboard')
#     return redirect('login')


# urlpatterns = [
#     path('admin/', admin.site.urls),

#     path('', home_redirect, name='home'),
#     path('', include('apps.accounts.urls')),
#     path('dashboard/', include('apps.dashboard.urls')),
# ]