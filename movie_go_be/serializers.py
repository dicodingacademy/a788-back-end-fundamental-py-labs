from rest_framework import serializers
from .models import Showtime, Reservation, ReservedSeat

class ShowtimeSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()
    studio = serializers.StringRelatedField()

    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'studio', 'start_time', 'end_time']

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