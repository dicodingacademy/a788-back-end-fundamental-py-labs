from django.urls import path
from . import views

urlpatterns = [
  path('movies/', views.MovieListCreateView.as_view(), name='movie-list'),
  path('movies/<uuid:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
  path('movies/upload/', views.MovieUploadView.as_view(), name='movie-upload'),
  path('movies/<uuid:pk>/images/', views.MovieImageView.as_view(), name='movie-image-list'),
]