from django.urls import path
from . import views

urlpatterns = [
  path('showtimes/', views.ShowtimeListCreateView.as_view()),
  path('showtimes/<uuid:pk>/', views.ShowtimeDetailView.as_view()),
  path('reservations/', views.ReservationListCreateView.as_view()),
  path('reservations/<uuid:pk>/', views.ReservationDetailView.as_view()),
  path('reserved-seats/', views.ReservedSeatListCreateView.as_view()),
  path('reserved-seats/<uuid:pk>/', views.ReservedSeatDetailView.as_view()),
]