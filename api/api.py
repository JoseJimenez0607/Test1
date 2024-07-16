from rest_framework import response
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status


class UserAPI (APIView):

    def post (self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return response(serializer.data, status = status.HTTP_400_BAD_REQUEST)