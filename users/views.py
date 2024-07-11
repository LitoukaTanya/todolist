from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, UserSoftDeleteSerializer


# представление для создания пользователя
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# представление для получения всех пользователей
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# представление для получения пользователя по ID
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# представление для изменения пользователя
class UserUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# представление для удаления пользователя
class UserDeleteView(APIView):

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if request.user.is_staff:
            user.delete()  # Жесткое удаление
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user == user:
            serializer = UserSoftDeleteSerializer(user, data={'is_active': False}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
