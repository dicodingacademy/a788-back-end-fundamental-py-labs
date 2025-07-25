from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Reservation, ReservedSeat
from reservations.serializers import ReservationSerializer, ReservedSeatSerializer
from django.http import Http404

# Create your views here.
class ReservationListCreateView(APIView):
    def get(self, request):
        reservations = Reservation.objects.all().order_by('reserved_at')[:10]
        serializer = ReservationSerializer(reservations, many=True)
        return Response({'reservations': serializer.data})

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationDetailView(APIView):
    def get_object(self, pk):
        try:
            reservation = Reservation.objects.get(pk=pk)
            self.check_object_permissions(self.request, reservation)
            return reservation
        except Reservation.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def put(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = self.get_object(pk)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReservedSeatListCreateView(APIView):
    def get(self, request):
        reserved_seats = ReservedSeat.objects.all().order_by('seat')[:10]
        serializer = ReservedSeatSerializer(reserved_seats, many=True)
        return Response({'reserved-seats': serializer.data})

    def post(self, request):
        serializer = ReservedSeatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservedSeatDetailView(APIView):
    def get_object(self, pk):
        try:
            reserved_seat = ReservedSeat.objects.get(pk=pk)
            self.check_object_permissions(self.request, reserved_seat)
            return reserved_seat
        except ReservedSeat.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        reserved_seat = self.get_object(pk)
        serializer = ReservedSeatSerializer(reserved_seat)
        return Response(serializer.data)

    def put(self, request, pk):
        reserved_seat = self.get_object(pk)
        serializer = ReservedSeatSerializer(reserved_seat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reserved_seat = self.get_object(pk)
        reserved_seat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)