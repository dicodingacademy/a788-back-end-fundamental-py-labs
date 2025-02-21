from rest_framework import serializers
from .models import Showtime

class ShowtimeSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()
    studio = serializers.StringRelatedField()

    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'studio', 'start_time', 'end_time']