from rest_framework import generics, authentication, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from user.serializers import UserSerializer, AuthTokenSerializer, PasswordResetSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in system view"""
    serializer_class = UserSerializer


class UpdateUserView(generics.RetrieveUpdateAPIView):
    """Update the user view"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CreateTokenView(ObtainAuthToken):
    """Create view for token"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


""" View to take email input """
class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.send_reset_email()
        return Response({"message": "Password reset email send"})


""" View to take new password as input vai reset link with given user id and token """
class PasswordResetConfirmationView(APIView):
    def post(self, request, user_id, token):
        user = self.get_user(user_id)
        if self.is_token_valid(user, token):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid reset token.'}, status=status.HTTP_400_BAD_REQUEST)

    """ Check if user with id exists """
    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            return None

    """ Check if token is valid """
    def is_token_valid(self, user, token):
        return default_token_generator.check_token(user, token)


