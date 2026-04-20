from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view, login_view, logout_view, home_view

urlpatterns = [

    path("signup/" , signup_view , name = 'signup'),

    path('login/' , login_view, name = 'login'),

    path('logout/' , logout_view , name = 'logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'registration/password_reset_form.html') , name = 'password_reset'),

    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name = 'registration/password_reset_done.html') , name = 'password_reset_done'),

    path('password-reset/confirm', auth_views.PasswordResetConfirmView.as_view(template_name = 'registration/password_reset_confirm.html') , name = 'password_reset_confirm'),

    path('password-reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name = 'registration/password_reset_form.html') , name = 'password_reset_complete'),

    path('', home_view, name='home'),
]







# from django.urls import path
# from django.contrib.auth import views as auth_views
# from .views import signup_view


# urlpatterns = [
#     path('signup/', signup_view, name='signup'),

#     path(
#         'login/',
#         auth_views.LoginView.as_view(template_name='login.html'),
#         name='login'
#     ),

#     path(
#         'logout/',
#         auth_views.LogoutView.as_view(),
#         name='logout'
#     ),

#     path(
#         'password-reset/',
#         auth_views.PasswordResetView.as_view(
#             template_name='registration/password_reset_form.html'
#         ),
#         name='password_reset'
#     ),

#     path(
#         'password-reset/done/',
#         auth_views.PasswordResetDoneView.as_view(
#             template_name='registration/password_reset_done.html'
#         ),
#         name='password_reset_done'
#     ),

#     path(
#         'reset/<uidb64>/<token>/',
#         auth_views.PasswordResetConfirmView.as_view(
#             template_name='registration/password_reset_confirm.html'
#         ),
#         name='password_reset_confirm'
#     ),

#     path(
#         'reset/done/',
#         auth_views.PasswordResetCompleteView.as_view(
#             template_name='registration/password_reset_complete.html'
#         ),
#         name='password_reset_complete'
#     ),
# ]