from rest_framework import serializers
from .models import Movie, MovieImage

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'overview', 'release_date', 'country', 'language', 'producer', 'director', 'duration', 'genre']

class MovieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieImage
        fields = ['id', 'movie', 'image']

    def validate_image(self, value):
        max_size = 2 * 1024 * 1024  # 2MB
        if value.size > max_size:
            raise serializers.ValidationError("Image size cannot exceed 2MB.")
        return value