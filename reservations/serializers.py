from rest_framework import serializers
from .models import Reservation, ReservedSeat

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'showtime', 'amount', 'reserved_at']

    def to_representation(self, value):
        """
        Override the to_representation method to return the user's username and the showtimes id.
        """
        return {
            'id': value.id,
            'user': value.user.username,
            'showtime': value.showtime.id,
            'amount': value.amount,
            'reserved_at': value.reserved_at
        }

class ReservedSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedSeat
        fields = ['id', 'seat', 'showtime', 'reservation']

    def to_representation(self, value):
        """
        Override the to_representation method to return the seat number, showtime id, and reservation id.
        """
        return {
            'id': value.id,
            'seat': value.seat.seat_number,
            'showtime': value.showtime.id,
            'reservation': value.reservation.id
        }