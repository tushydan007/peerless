from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from .tasks import send_verification_email
    



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_verified', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.is_active = False
        send_verification_email.delay(user.id)
        return user

    
    def validate(self, data):
        if User.objects.get(email=data['email']).exist():
            return serializers.ValidationError("User already exists")
        return data
        
    
    
    
class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        User = get_user_model()
        username_or_email = data['username_or_email'].lower()
        password = data['password']
        user = User.objects.filter(models.Q(username__iexact=username_or_email) | models.Q(email__iexact=username_or_email)).first()
        
        if user and user.locked_until > now():
            raise serializers.ValidationError('Account is locked. Try again later after 2 minutes.')
        
        if user and user.check_password(password):
            user.failed_login_attempts = 0
            user.locked_until = None
            user.save()
            return user
        else:
            if user:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 3:
                    user.locked_until = now() + timedelta(minutes=2)  # Lock for 10 minutes
                user.save()
            raise serializers.ValidationError('Invalid credentials.')
