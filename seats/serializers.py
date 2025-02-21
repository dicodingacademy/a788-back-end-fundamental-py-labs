from rest_framework import serializers
from .models import Seat

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'studio', 'seat_number']

    def to_representation(self, value):
        """
        Override the to_representation method to return the studio's name.
        """
        return {
            'id': value.id,
            'studio': value.studio.name,
            'seat_number': value.seat_number
        }