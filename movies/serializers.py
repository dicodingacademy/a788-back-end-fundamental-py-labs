from rest_framework import serializers
from .models import Movie, MovieImage

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'overview', 'release_date', 'country', 'language', 'producer', 'director', 'duration', 'genre']

    def to_representation(self, value):
        """
        Override the to_representation method to return the movie's image.
        """
        return {
            'id': value.id,
            'name': value.name,
            'overview': value.overview,
            'release_date': value.release_date,
            'country': value.country,
            'language': value.language,
            'producer': value.producer,
            'director': value.director,
            'duration': value.duration,
            'genre': value.genre,
            'image': value.movieimage_set.first().image.url if value.movieimage_set.first() else None
        }

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieImage
        fields = ['id', 'movie', 'image']

    def validate_image(self, value):
        # Contoh: batasi ukuran file
        max_size = 2 * 1024 * 1024  # 2MB
        if value.size > max_size:
            raise serializers.ValidationError("Image size cannot exceed 2MB.")
        return value