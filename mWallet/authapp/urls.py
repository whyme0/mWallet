from django.urls import path

from . import views

app_name = 'authapp'
urlpatterns = [
    path('logout/', views.log_out, name='logout'),
]
