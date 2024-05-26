from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import PasswordResetSerializer

class PasswordResetView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"

            message = render_to_string('password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })

            send_mail(
                'Password Reset Request',
                message,
                'from@example.com',
                [user.email],
                fail_silently=False,
            )

        return Response({'message': 'Password reset link sent.'}, status=status.HTTP_200_OK)


from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import SetNewPasswordSerializer

class PasswordResetConfirmView(generics.UpdateAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'message': 'Password has been reset.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)
