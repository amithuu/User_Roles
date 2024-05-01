from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from django.contrib.auth.models import User
from.models import Role

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email','is_active']

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        
        

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name',]

    def create(self, validated_data):
        return Role.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        
        
        
        