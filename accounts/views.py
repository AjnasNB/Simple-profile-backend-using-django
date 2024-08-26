import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from .serializers import (
    RegisterSerializer, 
    UserSerializer, 
    UpdateUserSerializer, 
    ResetPasswordEmailRequestSerializer
)
from rest_framework.permissions import IsAuthenticated
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Configure logging
logger = logging.getLogger(__name__)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not user.check_password(current_password):
            logger.warning(f"Password change failed for user {user.email}: Incorrect current password.")
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        logger.info(f"Password changed successfully for user {user.email}.")
        return Response({'success': 'Password updated successfully'}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [] 

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            logger.info(f"New user registered: {response.data['email']}")
        else:
            logger.error(f"Failed to register user: {request.data.get('email', 'unknown')} - {response.data}")
        return response


@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info(f"Profile updated for user {self.request.user.email}")
        else:
            logger.error(f"Failed to update profile for user {self.request.user.email} - {response.data}")
        return response


@method_decorator(csrf_exempt, name='dispatch')
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            logger.info(f"Password reset email requested for {request.data['email']}")
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            logger.error(f"Failed to request password reset for {request.data.get('email', 'unknown')} - {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                logger.warning(f"Invalid password reset token for user ID {id}.")
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            logger.info(f"Valid password reset token for user ID {id}.")
            return Response({'success': True, 'message': 'Credentials valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            logger.error("Failed to decode user ID during password reset token check.")
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Profile updated successfully for user {user.email}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            logger.error(f"Failed to update profile for user {user.email} - {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class ListUsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterSerializer
        return UserSerializer

    def delete(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            logger.info(f"User {user.email} deleted successfully.")
            return Response({'success': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error(f"Attempted to delete non-existent user ID {pk}.")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteUserView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            logger.info(f"User {user.email} deleted successfully.")
            return Response({'success': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error(f"Attempted to delete non-existent user ID {pk}.")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
