from django.shortcuts import render
from rest_framework.views import APIView as ApiView
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication

class login(ApiView):
    def post(self, request):
        try:
            user = get_object_or_404(User, username=request.data['username'])
            if not user.check_password(request.data['password']):
                return Response({"detail": 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(instance = user)
            return Response({"token": token.key}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(f"Error during login: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class signup(ApiView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(username=request.data['username'])
                user.set_password(request.data['password'])

                user.save()
                token = Token.objects.create(user=user)
                return Response({"token": token.key}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error during signup: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class logout(ApiView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error during logout: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class validate_token(ApiView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({"message": "Token is valid for: " + user.username}, status=status.HTTP_200_OK)
