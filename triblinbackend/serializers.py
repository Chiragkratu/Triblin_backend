from django.contrib.auth import authenticate
from django.contrib.auth.models import User 
from rest_framework import serializers
from .models import Location, Plastic_Item
from .models import Messages

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data.get('email', ''),
            validated_data['password']
        )
        return user



class PlasticItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plastic_Item
        fields = '__all__'

class LocationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
