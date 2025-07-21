from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.exceptions import APIException # type: ignore
from rest_framework import status # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from django.shortcuts import get_object_or_404

from .models import KayakUser
from .serializers import KayakUsersSerializer

class UserNotFoundException(APIException):
    status_code = 404
    default_detail = 'User not found.'
    default_code = 'user_not_found'

class KayakUsersAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Allow any user to access this API

    # This queryset is used to fetch all trips, ordered by start time.
    # It can be overridden in the get method if specific filtering is needed.
    # Note: This queryset does not filter by user, so it may include private trips.
    # Filtering for private trips is handled in the get method.
    queryset = KayakUser.objects.all()
    serializer_class = KayakUsersSerializer

    def get(self, request):
        users = self.queryset.all()
            
        if not users: # If no users are left after filtering, return a 404
                raise UserNotFoundException()
        
        if 'fields' in request.GET:
            if request.GET['fields'] == 'all':
                fields = None
        else:
            if 'field' in request.GET:
                if request.GET['field'] == 'all':
                    fields = None
                else:
                    fields = request.GET.getlist('field')
                    fields.append('id')  # always include the ID field
            else:
                fields = ('id', 'email')  # default fields

        serializer = KayakUsersSerializer(users, many=True, fields=fields)
        return Response(serializer.data)

    def post(self, request):
        serializer = KayakUsersSerializer(data=request.data)
        if serializer.is_valid():
            trip = serializer.save()
            return Response(KayakUsersSerializer(trip).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
