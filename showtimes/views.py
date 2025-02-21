from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from core.permissions import IsAdminOrStudioManagerOrSuperUser
from .models import Showtime
from .serializers import ShowtimeSerializer

# Create your views here.
class ShowtimeListCreateView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminOrStudioManagerOrSuperUser()]
        return [IsAuthenticated()]

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
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method != 'GET':
            return [IsAuthenticated(), IsAdminOrStudioManagerOrSuperUser()]
        return [IsAuthenticated()]

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