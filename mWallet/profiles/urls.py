from django.urls import path

from profiles import views

app_name = 'profiles'
urlpatterns = [
    path('', views.ProfileView.as_view(), name='current_profile'),
    path('edit/', views.EditProfile.as_view(), name='edit_profile'),
    path('edit/deleting', views.PersonDeleteConfirmation.as_view(), name='profile_deleting'),
    path('edit/deleting/delete', views.PersonDelete.as_view(), name='profile_delete'),
    path('wallets/', views.WalletsView.as_view(), name='profile_wallets'),
    path('wallets/create', views.WalletCreationView.as_view(), name='wallet_creation'),
    path('wallets/<int:pk>', views.WalletInfoView.as_view(), name='current_wallet'),
    path('wallets/<int:pk>/edit', views.WalletEditView.as_view(), name='wallet_edit'),
    path('wallets/<int:pk>/delete', views.WalletDelete.as_view(), name='wallet_delete'),
    path('wallets/<int:pk>/operation-create', views.OperationCreateView.as_view(), name='operation_create'),
]
