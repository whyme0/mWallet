from django.urls import path

from . import views

app_name = 'authapp'
urlpatterns = [
    path('logout/', views.log_out, name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
]
