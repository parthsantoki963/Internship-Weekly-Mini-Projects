from rest_framework import serializers
from .models import Job
from .tasks import send_welcome_email
from .models import JobSeeker
from django.contrib.auth.models import User


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    # This ensures the password hides as *** when typing and doesn't get sent back in the API response
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        # 1. Create the base User securely
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        # 2. Automatically generate the JobSeeker profile and subscribe them!
        JobSeeker.objects.create(
            user=user,
            is_subscribed=True,
            keywords="Remote, General" # Default keywords
        )
        
        # 3. Trigger the welcome email in the background!
        if user.email:
            send_welcome_email.delay(user.email, user.username)
        
        return user