from django.urls import path
from . import views

urlpatterns = [
  path('showtimes/', views.ShowtimeListCreateView.as_view()),
  path('showtimes/<uuid:pk>/', views.ShowtimeDetailView.as_view()),
]