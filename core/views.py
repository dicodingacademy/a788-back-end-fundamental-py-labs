from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminOrSuperUser, IsOwnerOrAdminOrSuperUser
from .models import User
from .serializers import UserSerializer, GroupSerializer
from django.http import Http404
from loguru import logger

class UserListCreateView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return []

    def get(self, request):
        users = User.objects.all().order_by('username')[:10]
        serializer = UserSerializer(users, many=True)
        return Response({'users': serializer.data})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Creating a new user with data: {}", request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminOrSuperUser()]
        return [IsAuthenticated(), IsOwnerOrAdminOrSuperUser()]

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except User.DoesNotExist:
            logger.info("User with ID {} not found", pk)
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Updating user with ID {} with data: {}", pk, request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        logger.info("Deleting user with ID {}", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    def get(self, request):
        groups = Group.objects.all().order_by('name')[:10]
        serializer = GroupSerializer(groups, many=True)
        return Response({'groups': serializer.data})

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Creating a new group with data: {}", request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    def get_object(self, pk):
        try:
            group = Group.objects.get(pk=pk)
            self.check_object_permissions(self.request, group)
            return group
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def put(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Updating group with ID {} with data: {}", pk, request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        group = self.get_object(pk)
        group.delete()
        logger.info("Deleting group with ID {}", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AssignRoleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    def post(self, request):
        user = get_object_or_404(User, pk=request.data['user_id'])
        group = get_object_or_404(Group, pk=request.data['group_id'])
        user.groups.add(group)
        logger.info("Assigned group {} to user {}", group.name, user.username)
        return Response(status=status.HTTP_201_CREATED)