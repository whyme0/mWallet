from django.urls import path

from profiles import views

app_name = 'profiles'
urlpatterns = [
    path('', views.ProfileView.as_view(), name='current_profile'),
    path('edit', views.EditProfile.as_view(), name='edit_profile'),
    path('edit/deleting', views.DeleteConfirmation.as_view(), name='profile_deleting'),
    path('edit/deleting/delete', views.Delete.as_view(), name='profile_delete'),
    path('wallets', views.WalletsView.as_view(), name='profile_wallets'),
    # path('wallets/create', views.WalletsCreation.as_view(), name='wallet_creation'),
]
