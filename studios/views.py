from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Studio, StudioManager
from .serializers import StudioSerializer, StudioManagerSerializer

# Create your views here.
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