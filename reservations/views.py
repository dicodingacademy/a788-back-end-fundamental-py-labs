from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from core.permissions import IsAdminOrSuperUser
from .models import Reservation, ReservedSeat
from reservations.serializers import ReservationSerializer, ReservedSeatSerializer

# Create your views here.
class ReservationListCreateView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]


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
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def put(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReservedSeatListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        reserved_seat = get_object_or_404(ReservedSeat, pk=pk)
        serializer = ReservedSeatSerializer(reserved_seat)
        return Response(serializer.data)

    def put(self, request, pk):
        reserved_seat = get_object_or_404(ReservedSeat, pk=pk)
        serializer = ReservedSeatSerializer(reserved_seat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reserved_seat = get_object_or_404(ReservedSeat, pk=pk)
        reserved_seat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)