from django.urls import path
from .views import (
    RegisterView, 
    UserProfileView, 
    RequestPasswordResetEmail, 
    PasswordTokenCheckAPI, 
    UpdateProfileView, 
    ListUsersView,
    ChangePasswordView,
    DeleteUserView,
    SetNewPasswordAPIView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name="password-reset-confirm"),
    path('set-new-password/<uidb64>/<token>/', SetNewPasswordAPIView.as_view(), name="set-new-password"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', ListUsersView.as_view(), name='user-list'),
    path('users/<int:pk>/', DeleteUserView.as_view(), name='user-delete'),
]
