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
    UserProfileSerializer,
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
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View


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


@api_view(["GET", "PUT"])
def user_profile(request):
    if request.method == "GET":
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    if request.method == "PUT":
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        # Get the transactions for the logged-in user
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class ChurchListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all churches
        """
        churches = Church.objects.all()
        serializer = ChurchSerializer(churches, many=True)
        return Response(serializer.data)


class ChurchDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Get details of a single church by ID
        """
        try:
            church = Church.objects.get(pk=pk)
        except Church.DoesNotExist:
            return Response(
                {"detail": "Church not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChurchSerializer(church)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a church
        """
        try:
            church = Church.objects.get(pk=pk)
        except Church.DoesNotExist:
            return Response(
                {"detail": "Church not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChurchSerializer(church, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a church by ID
        """
        try:
            church = Church.objects.get(pk=pk)
            church.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Church.DoesNotExist:
            return Response(
                {"detail": "Church not found."}, status=status.HTTP_404_NOT_FOUND
            )


class ChurchCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create a new church
        """
        serializer = ChurchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        """
        Create a new transaction for the authenticated user
        """
        # Add the user to the request data
        data = request.data.copy()
        data["user"] = (
            request.user.id
        )  # Automatically assign the authenticated user to the transaction

        # Ensure the church_id is provided in the request data (required for ForeignKey)
        if "church_id" not in data:
            return Response(
                {"error": "church_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Validate and create the transaction
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
