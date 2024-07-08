from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Task
from app.serializers import TaskSerializer


class TaskCreateView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(created_by=user, deleted=False)


class TaskListByStatus(generics.ListAPIView):
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status:
            return Task.objects.filter(status=status)
        else:
            return Task.objects.none()
