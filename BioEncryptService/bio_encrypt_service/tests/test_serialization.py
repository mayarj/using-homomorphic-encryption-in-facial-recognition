from django.test import TestCase
from ..serializers import *


class TestSerialization(TestCase):
    def setUp(self):
        print ( " regestration test ")
        request_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            
        }
        
        serializer = UserSerializer(data=request_data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
           
        else:
            print(serializer.errors)

    def test_login(self):
        print ( " log in  test ")
        request_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        serializer = CustomTokenObtainPairSerializer(data=request_data)
        if serializer.is_valid():
            data = serializer.validated_data
            print(data)
        else:
            print(serializer.errors)
