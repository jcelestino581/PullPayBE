from rest_framework import generics, viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.contrib.auth import get_user_model, authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction, User, Church
from .serializers import (
    TransactionSerializer,
    UserSerializer,
    ChurchSerializer,
    UserRegistrationSerializer,
    ProfileSerializer,
)
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can access

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(["GET"])
def get_profile(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED
        )

    user = request.user  # The authenticated user
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }

    return Response(user_data)


@api_view(["PUT"])
def update_profile(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED
        )

    user = request.user  # The authenticated user

    # Update the user's fields
    user.first_name = request.data.get("first_name", user.first_name)
    user.last_name = request.data.get("last_name", user.last_name)
    user.email = request.data.get("email", user.email)

    # Save the updated user
    try:
        user.save()
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        return Response(user_data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Handle GET request
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        # Handle PUT request (updating user profile)
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
