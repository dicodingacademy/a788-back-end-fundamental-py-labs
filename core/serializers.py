from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        """
        Override the create method to hash the password.
        """
        password = validated_data.pop('password')
        hashed_password = make_password(password)

        user = User.objects.create(
            username=validated_data['username'],
            password=hashed_password
        )

        return user

    def to_representation(self, value):
        """
        Override the to_representation method to return the user's groups.
        """
        return {
            'id': value.id,
            'username': value.username,
            'email': value.email,
            'first_name': value.first_name,
            'last_name': value.last_name,
            'groups': value.groups.values_list('name', flat=True)
        }
