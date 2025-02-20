from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Studio, StudioManager, Seat, Showtime, Reservation, ReservedSeat
from .serializers import StudioSerializer, StudioManagerSerializer, SeatSerializer, ShowtimeSerializer, ReservationSerializer, ReservedSeatSerializer

class StudioListCreateView(APIView):
    def get(self, request):
        studios = Studio.objects.all().order_by('name')[:10]
        serializer = StudioSerializer(studios, many=True)
        return Response({'studios': serializer.data})

    def post(self, request):
        serializer = StudioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudioDetailView(APIView):
    def get(self, request, pk):
        studio = get_object_or_404(Studio, pk=pk)
        serializer = StudioSerializer(studio)
        return Response(serializer.data)

    def put(self, request, pk):
        studio = get_object_or_404(Studio, pk=pk)
        serializer = StudioSerializer(studio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        studio = get_object_or_404(Studio, pk=pk)
        studio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StudioManagerListCreateView(APIView):
    def get(self, request):
        studio_managers = StudioManager.objects.select_related('user', 'studio').all().order_by('user__username')[:10]
        serializer = StudioManagerSerializer(studio_managers, many=True)
        return Response({'studio-managers': serializer.data})

    def post(self, request):
        serializer = StudioManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudioManagerDetailView(APIView):
    def get(self, request, pk):
        studio_manager = get_object_or_404(StudioManager, pk=pk)
        serializer = StudioManagerSerializer(studio_manager)
        return Response(serializer.data)

    def put(self, request, pk):
        studio_manager = get_object_or_404(StudioManager, pk=pk)
        serializer = StudioManagerSerializer(studio_manager, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        studio_manager = get_object_or_404(StudioManager, pk=pk)
        studio_manager.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SeatListCreateView(APIView):
    def get(self, request):
        seats = Seat.objects.all().order_by('seat_number')[:10]
        serializer = SeatSerializer(seats, many=True)
        return Response({'seats': serializer.data})

    def post(self, request):
        serializer = SeatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SeatDetailView(APIView):
    def get(self, request, pk):
        seat = get_object_or_404(Seat, pk=pk)
        serializer = SeatSerializer(seat)
        return Response(serializer.data)

    def put(self, request, pk):
        seat = get_object_or_404(Seat, pk=pk)
        serializer = SeatSerializer(seat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        seat = get_object_or_404(Seat, pk=pk)
        seat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ShowtimeListCreateView(APIView):
    def get(self, request):
        showtimes = Showtime.objects.all().order_by('start_time')[:10]
        serializer = ShowtimeSerializer(showtimes, many=True)
        return Response({'showtimes': serializer.data})

    def post(self, request):
        serializer = ShowtimeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowtimeDetailView(APIView):
    def get(self, request, pk):
        showtime = get_object_or_404(Showtime, pk=pk)
        serializer = ShowtimeSerializer(showtime)
        return Response(serializer.data)

    def put(self, request, pk):
        showtime = get_object_or_404(Showtime, pk=pk)
        serializer = ShowtimeSerializer(showtime, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        showtime = get_object_or_404(Showtime, pk=pk)
        showtime.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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