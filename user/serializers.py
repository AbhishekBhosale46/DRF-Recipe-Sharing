from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Updatet the user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password('password', None)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password,
        )

        if not user:
            msg = _('Unable to authorize the user with provided crendentials')
            raise serializers.ValidationError(msg, code = 'authorization')

        attrs['user'] = user
        return attrs

""" This serializer is to take email input, validate it and then send email"""
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    """ Function to validate email """
    def validate_email(self,value):
            user_model = get_user_model()
            try:
                user = user_model.objects.get(email = value)
            except user_model.DoesNotExist:
                raise serializers.ValidationError(_("User with given email doesnt exists"))
            return value

    """ Function to send email """
    def send_reset_email(self):
        email = self.validated_data['email']
        user = get_user_model().objects.get(email=email)
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.FRONTEND_URL}/reset/{user.id}/{token}/"
        subject = "Password reset request"
        message = f"Click link to reset password {reset_url}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)


