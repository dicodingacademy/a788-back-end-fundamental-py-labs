from django.urls import path
from . import views

urlpatterns = [
  path('movies/', views.MovieListCreateView.as_view()),
  path('movies/<uuid:pk>/', views.MovieDetailView.as_view()),
  path('studios/', views.StudioListCreateView.as_view()),
  path('studios/<uuid:pk>/', views.StudioDetailView.as_view()),
  path('studio-managers/', views.StudioManagerListCreateView.as_view()),
  path('studio-managers/<uuid:pk>/', views.StudioManagerDetailView.as_view()),
  path('seats/', views.SeatListCreateView.as_view()),
  path('seats/<uuid:pk>/', views.SeatDetailView.as_view()),
  path('showtimes/', views.ShowtimeListCreateView.as_view()),
  path('showtimes/<uuid:pk>/', views.ShowtimeDetailView.as_view()),
  path('reservations/', views.ReservationListCreateView.as_view()),
  path('reservations/<uuid:pk>/', views.ReservationDetailView.as_view()),
  path('reserved-seats/', views.ReservedSeatListCreateView.as_view()),
  path('reserved-seats/<uuid:pk>/', views.ReservedSeatDetailView.as_view()),
]