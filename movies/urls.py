from django.urls import path
from . import views

urlpatterns = [
  path('movies/', views.MovieListCreateView.as_view()),
  path('movies/<uuid:pk>/', views.MovieDetailView.as_view()),
]