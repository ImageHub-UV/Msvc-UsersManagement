from .models import User
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

class UserViewSet(APIView):
    queryset = User.objects.all()
    
    def get(self, request,id):
        with transaction.atomic():           
            try:
                user = User.objects.get(id=id)
                serializer_data = UserSerializer(user)
                return Response(serializer_data.data,status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                