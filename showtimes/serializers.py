from rest_framework import serializers
from .models import Showtime

class ShowtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'studio', 'start_time', 'end_time']

    def to_representation(self, value):
        """
        Override the to_representation method to return the movie's name and the studio's name.
        """
        return {
            'id': value.id,
            'movie': value.movie.name,
            'studio': value.studio.name,
            'start_time': value.start_time,
            'end_time': value.end_time
        }