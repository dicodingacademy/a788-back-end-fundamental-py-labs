from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'overview', 'release_date', 'country', 'language', 'producer', 'director', 'duration', 'genre']