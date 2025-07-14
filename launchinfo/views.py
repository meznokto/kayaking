from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Launch, LaunchImage
from .serializers import LaunchSerializer


class ListLaunches(APIView):
    queryset = Launch.objects.all().order_by('-date_updated')
    serializer_class = LaunchSerializer

    def get(self, request):
        launches = self.queryset.all()
        serializer = self.serializer_class(launches, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            launch = serializer.save()
            return Response(LaunchSerializer(launch).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        launch = get_object_or_404(Launch, pk=pk)
        serializer = self.serializer_class(launch, data=request.data)
        if serializer.is_valid():
            updated_launch = serializer.save()
            return Response(LaunchSerializer(updated_launch).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
