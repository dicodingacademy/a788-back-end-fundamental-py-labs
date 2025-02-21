from django.urls import path
from . import views

urlpatterns = [
  path('users/', views.UserListCreateView.as_view()),
  path('users/<uuid:pk>/', views.UserDetailView.as_view()),
  path('groups/', views.GroupListCreateView.as_view()),
  path('groups/<int:pk>/', views.GroupDetailView.as_view()),
  path('assign-roles/', views.AssignRoleView.as_view()),
]