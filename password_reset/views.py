from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from .serializers import PasswordResetSerializer, SetNewPasswordSerializer
from django.conf import settings
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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
            User = get_user_model()
            user = User.objects.filter(email=email).first()

            if user:
                logger.info(f"User found: {user.username}")
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

                message = render_to_string('password_reset_email.txt', {
                    'user': user,
                    'reset_url': reset_url,
                })

                html_message = render_to_string('password_reset_email.html', {
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
                    html_message=html_message
                )
                logger.info("Email sent successfully")
            else:
                logger.info(f"No user found with email: {email}")
                return Response({'email': ['No user found with this email address.']}, status=status.HTTP_400_BAD_REQUEST)

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
            User = get_user_model()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
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




User = get_user_model()

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"old_password": ["Old password is not correct."]}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password has been changed."}, status=status.HTTP_200_OK)
