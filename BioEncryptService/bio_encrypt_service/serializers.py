from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .models import UserProfile  # Import the UserProfile model

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles the creation of new users and their profiles.
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]# Ensure email is unique
    )
    password = serializers.CharField(write_only=True, required=True)# Password is write-only
    hashing_type = serializers.ChoiceField(
        choices=list(settings.HASHING_CLASSES.keys()), # Choices for hashing types
        default=next(iter( settings.HASHING_CLASSES)) # Default to the first hashing type
    )
    encryption_type = serializers.ChoiceField(
        choices=list(settings.ENCRYPTION_CLASSES.keys()),# Choices for encryption types
        default=next(iter(settings.ENCRYPTION_CLASSES)) # Default to the first encryption type
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'hashing_type', 'encryption_type']

    def create(self, validated_data):
        """
        Create a new user and their profile.

        Args:
            validated_data: Validated data from the serializer.

        Returns:
            dict: User data and tokens.
        """

        # Extract hashing and encryption types from the validated data
        hashing_type = validated_data.pop('hashing_type')
        encryption_type = validated_data.pop('encryption_type')

        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Create the user profile with the selected hashing and encryption types
        UserProfile.objects.create(user=user, hashing_type=hashing_type, encryption_type=encryption_type)
        
        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)

        #  Return user data and tokens
        return {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'hashing_type': hashing_type,
            'encryption_type': encryption_type,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining JWT tokens.
    Adds custom claims to the token and includes additional user data in the response.
    """

    @classmethod
    def get_token(cls, user):
        """
        Generate a token with custom claims.

        Args:
            user: The user for whom the token is generated.

        Returns:
            Token: A JWT token with custom claims.
        """
        token = super().get_token(user)
        # Add custom claims to the token
        token['username'] = user.username
        token['email'] = user.email
        token['user_id'] = user.id
        return token

    def validate(self, attrs):
        """
        Validate the user credentials and return tokens with additional user data.

        Args:
            attrs: Input data (username and password).

        Returns:
            dict: Tokens and additional user data.
        """
        # Validate the credentials and get the tokens
        data = super().validate(attrs)
        # Add custom response data
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        
        return data
