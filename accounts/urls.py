from django.urls import path
from .views import (
    RegisterView, 
    UserProfileView, 
    RequestPasswordResetEmail, 
    PasswordTokenCheckAPI, 
    UpdateProfileView, 
    ListUsersView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name="password-reset-confirm"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/users/', ListUsersView.as_view(), name='admin-user-list'),  # This is the important line
]
