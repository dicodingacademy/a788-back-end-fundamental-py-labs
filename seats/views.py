from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Seat
from .serializers import SeatSerializer

# Create your views here.
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
