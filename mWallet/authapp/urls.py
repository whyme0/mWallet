from django.urls import path

from . import views

app_name = 'authapp'
urlpatterns = [
    path('logout/', views.log_out, name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', views.AskEmailView.as_view(), name='ask_email'),
    path('password-reset/<str:token>/', views.PasswordResetView.as_view(), name='password_reset')
]
