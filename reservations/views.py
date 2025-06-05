from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import Http404
from core.permissions import IsAdminOrSuperUser
from .models import Reservation, ReservedSeat
from reservations.serializers import ReservationSerializer, ReservedSeatSerializer
from .tasks import send_ticket_email
from loguru import logger

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
            reservation = serializer.save()
            logger.info(f"Reservation {reservation.id} created by {reservation.user.username}")
            send_ticket_email.delay(reservation.user.email, reservation.user.username, reservation.id)
            logger.info(f"Sending ticket email to {reservation.user.email} for reservation {reservation.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            reservation = Reservation.objects.get(pk=pk)
            self.check_object_permissions(self.request, reservation)
            return reservation
        except Reservation.DoesNotExist:
            logger.info(f"Reservation with ID {pk} not found")
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
            logger.info(f"Reservation {reservation.id} updated by {reservation.user.username}")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = self.get_object(pk)
        reservation.delete()
        logger.info(f"Reservation {reservation.id} deleted by {reservation.user.username}")
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
            logger.info(f"Reserved seat {serializer.data['id']} created for reservation {serializer.data['reservation']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservedSeatDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            reserved_seat = ReservedSeat.objects.get(pk=pk)
            self.check_object_permissions(self.request, reserved_seat)
            return reserved_seat
        except ReservedSeat.DoesNotExist:
            logger.info(f"Reserved seat with ID {pk} not found")
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
            logger.info(f"Reserved seat {reserved_seat.id} updated for reservation {reserved_seat.reservation.id}")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reserved_seat = self.get_object(pk)
        reserved_seat.delete()
        logger.info(f"Reserved seat {reserved_seat.id} deleted for reservation {reserved_seat.reservation.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)