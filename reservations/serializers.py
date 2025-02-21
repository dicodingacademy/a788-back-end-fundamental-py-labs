from rest_framework import serializers
from .models import Reservation, ReservedSeat

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    showtime = serializers.StringRelatedField()

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'showtime', 'amount', 'reserved_at']

class ReservedSeatSerializer(serializers.ModelSerializer):
    seat = serializers.StringRelatedField()
    showtime = serializers.StringRelatedField()
    reservation = serializers.StringRelatedField()

    class Meta:
        model = ReservedSeat
        fields = ['id', 'seat', 'showtime', 'reservation']