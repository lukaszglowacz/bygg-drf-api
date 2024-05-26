from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from .serializers import PasswordResetSerializer, SetNewPasswordSerializer
from accounts.models import CustomUser  # Zaktualizowany import niestandardowego modelu użytkownika
import logging

logger = logging.getLogger(__name__)

class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info("Received password reset request")
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Validation error: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            email = serializer.validated_data['email']
            logger.info(f"Looking for user with email: {email}")
            user = CustomUser.objects.filter(email=email).first()

            if user:
                logger.info(f"User found: {user.username}")
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f"{request.scheme}://{request.get_host()}/password-reset/confirm/{uid}/{token}/"  # Aktualizacja reset_url

                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })

                logger.info(f"Sending password reset email to {user.email}")
                send_mail(
                    'Password Reset Request',
                    message,
                    'from@example.com',
                    [user.email],
                    fail_silently=False,
                )
                logger.info("Email sent successfully")
            else:
                logger.info(f"No user found with email: {email}")

            return Response({'message': 'Password reset link sent.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error during password reset: {e}", exc_info=True)
            return Response({'error': 'An error occurred during password reset.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetConfirmView(APIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)  # Użycie niestandardowego modelu użytkownika
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
            logger.error(f"Error decoding UID or finding user: {e}", exc_info=True)
            user = None

        if user and default_token_generator.check_token(user, token):
            serializer = self.serializer_class(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({'message': 'Password has been reset.'}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error saving new password: {e}", exc_info=True)
                return Response({'error': 'An error occurred while resetting the password.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error(f"Invalid link for password reset: UID={uidb64}, Token={token}")
            return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)
