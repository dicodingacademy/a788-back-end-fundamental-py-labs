from rest_framework import serializers
from .models import Studio, StudioManager

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['id', 'name', 'seat_capacity']

class StudioManagerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    studio = serializers.StringRelatedField()

    class Meta:
        model = StudioManager
        fields = ['id', 'user', 'studio']