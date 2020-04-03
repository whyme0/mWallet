from django.urls import path

from profiles import views

app_name = 'profiles'
urlpatterns = [
    path('', views.ProfileView.as_view(), name='current_profile'),
    path('edit', views.EditProfile.as_view(), name='edit_profile'),
]
