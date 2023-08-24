from rest_framework import serializers
from .models import CustomUser, Profile



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'





class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {"confirm_password": {"write_only": True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
            # return data
        
        if len(data) > 5:
            raise serializers.ValidationError("Password must be at least 5 characters long.")
        return data
 
        
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {"confirm_password": {"write_only": True}}




class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)