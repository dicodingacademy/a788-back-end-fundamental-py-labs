from django.urls import path
from . import views

urlpatterns = [
  path('studios/', views.StudioListCreateView.as_view()),
  path('studios/<uuid:pk>/', views.StudioDetailView.as_view()),
  path('studio-managers/', views.StudioManagerListCreateView.as_view()),
  path('studio-managers/<uuid:pk>/', views.StudioManagerDetailView.as_view()),
]