from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from .models import Transaction, User, Church
from .serializers import (
    TransactionSerializer,
    UserSerializer,
    ChurchSerializer,
    UserRegistrationSerializer,
)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ChurchViewSet(viewsets.ModelViewSet):
    queryset = Church.objects.all()
    serializer_class = UserSerializer


@api_view(["POST"])
def register_user(request):
    # Retrieve the data from the request body
    data = request.data

    # Retrieve the fields
    first_name = data.get("first_name")  # camelCase from the frontend
    last_name = data.get("last_name")  # camelCase from the frontend
    email = data.get("email")
    password = data.get("password")
    churches = data.get("churches", [])

    # Ensure all fields are provided
    if not all([first_name, last_name, email, password]):
        return Response(
            {"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the email already exists
    if get_user_model().objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST
        )

    # Create the user with snake_case field names for Django
    user = get_user_model().objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    # Add the user to the churches
    for church_name in churches:
        try:
            church = Church.objects.get(name=church_name)
            user.churches.add(church)
        except Church.DoesNotExist:
            return Response(
                {"error": f"Church with name {church_name} does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Return a success message
    return Response(
        {"message": "User registered successfully!"}, status=status.HTTP_201_CREATED
    )


# Create a list view for all transactions
class TransactionListView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


# Create a detail view for a single transaction
class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


# Create a list view for all users
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Create a detail view for a single user
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
