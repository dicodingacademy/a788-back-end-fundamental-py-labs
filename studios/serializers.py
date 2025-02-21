from rest_framework import serializers
from .models import Studio, StudioManager

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['id', 'name', 'seat_capacity']

class StudioManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioManager
        fields = ['id', 'user', 'studio']

    def to_representation(self, value):
        """
        Override the to_representation method to return the user's username and the studio's name.
        """
        return {
            'id': value.id,
            'user': value.user.username,
            'studio': value.studio.name
        }