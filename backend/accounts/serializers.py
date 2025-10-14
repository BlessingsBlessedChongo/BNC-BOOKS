from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from .models import User, UserProfile
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'password_confirm', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate_first_name(self, value):
        if len(value) < 2 or len(value) > 30:
            raise serializers.ValidationError("First name must be between 2 and 30 characters.")
        if not re.match(r'^[A-Za-z\s]+$', value):
            raise serializers.ValidationError("First name can only contain letters and spaces.")
        return value
    
    def validate_last_name(self, value):
        if len(value) < 2 or len(value) > 30:
            raise serializers.ValidationError("Last name must be between 2 and 30 characters.")
        if not re.match(r'^[A-Za-z\s]+$', value):
            raise serializers.ValidationError("Last name can only contain letters and spaces.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value
    
    def validate_password(self, value):
        # Required field validation
        if not value:
            raise serializers.ValidationError("This field is required.")
        
        # Length validation
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters.")
        
        # Uppercase validation
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        
        # Number validation
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        
        # Special character validation
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        # Django's built-in password validation
        validate_password(value)
        return value
    
    def validate_role(self, value):
        valid_roles = ['buyer', 'seller', 'affiliate']
        if value not in valid_roles:
            raise serializers.ValidationError("Invalid role. Must be 'buyer', 'seller', or 'affiliate'.")
        return value
    
    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': ['Passwords do not match.']
            })
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Set username to email for email-based authentication
        username = validated_data['email']
        validated_data['username'] = username
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Use get_or_create to avoid duplicate UserProfile
        UserProfile.objects.get_or_create(user=user)
        
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value
    
    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
    def validate_new_password(self, value):
        # Reuse the same password validation as registration
        if not value:
            raise serializers.ValidationError("This field is required.")
        
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters.")
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        validate_password(value)
        return value
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': ['New passwords do not match.']
            })
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('store_name', 'bio', 'location', 'birth_date', 'avatar')

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'is_active', 'date_joined', 'profile')
        read_only_fields = ('id', 'is_active', 'date_joined')

class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class UserWithTokensSerializer(serializers.Serializer):
    user = UserSerializer()
    tokens = TokenSerializer()