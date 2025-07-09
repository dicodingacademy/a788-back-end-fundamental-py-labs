import json
import os
import tempfile
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.permissions import IsAdminOrSuperUser
from .models import Movie
from .serializers import MovieSerializer, MoviePosterSerializer
from minio import Minio
from django.core.cache import cache
from loguru import logger

def get_minio_client():
    return Minio(
        endpoint=os.getenv('MINIO_ENDPOINT_URL'),
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=False
    )


bucket_name = os.getenv('MINIO_BUCKET_NAME')
CACHE_KEY_LIST = "movie_list"
CACHE_KEY_DETAIL = "movie_detail_{}"

# Create your views here.
class MovieListCreateView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get(self, request):
        movies = cache.get(CACHE_KEY_LIST)

        # Jika tidak ada di cache, ambil dari database
        if not movies:
            print("Data diambil dari database...")
            data = Movie.objects.all().order_by('name')[:10]
            cache.get(CACHE_KEY_LIST)
            serializer = MovieSerializer(data, many=True)

            # Serialisasi data ke JSON string
            movies_data = json.dumps(serializer.data)

            # Simpan di Redis selama 15 menit
            cache.set(CACHE_KEY_LIST, movies_data, timeout=60 * 15)

            movies = movies_data
            data_source = "database"
        else:
            print("Data diambil dari cache...")
            data_source = "cache"

        # Kembalikan hasil response dalam bentuk JSON
        response = Response({'movies': json.loads(movies)})
        response['X-Data-Source'] = data_source
        return response

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(CACHE_KEY_LIST)
            logger.info("Creating a new movie with data: {}", request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieDetailView(APIView):
    def get_object(self, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            self.check_object_permissions(self.request, movie)
            return movie
        except Movie.DoesNotExist:
            logger.info("Movie with ID {} not found", pk)
            raise Http404

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method != 'GET':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated()]

    def get(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Updating movie with ID {} with data: {}", pk, request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()
        logger.info("Deleting movie with ID {}", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MoviePosterView(APIView):
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        return [IsAuthenticated(), IsAdminOrSuperUser()]

    def post(self, request):
        serializer = MoviePosterSerializer(data=request.data)
        file = request.data.get('image')

        if serializer.is_valid():
            serializer.save()

            # Simpan file sementara sebelum upload ke Minio
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            try:
                object_name = f"{serializer.instance.image.name}"
                client = get_minio_client()
                client.fput_object(bucket_name, object_name, temp_file_path, content_type=file.content_type)
            except Exception as e:
                logger.error(f"Upload to Minio failed: {str(e)}")
                return Response(
                    {"error": f"Upload to Minio failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                os.remove(temp_file_path)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MoviePosterDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        images = movie.movieimage_set.all()

        serialized_images = []
        for image in images:
            client = get_minio_client()
            presigned_url = client.presigned_get_object(
                bucket_name,
                image.image.name,
                response_headers={"response-content-type": "image/jpeg"}
            )
            serialized_images.append({"id": image.id, "url": presigned_url})

        return Response(serialized_images)