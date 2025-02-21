from rest_framework import serializers
from .models import Seat

class SeatSerializer(serializers.ModelSerializer):
    studio = serializers.StringRelatedField()

    class Meta:
        model = Seat
        fields = ['id', 'studio', 'seat_number']