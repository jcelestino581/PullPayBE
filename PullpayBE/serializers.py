from rest_framework import serializers
from .models import User, Transaction, Church  # Import the models


# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "firstName",
            "lastName",
            "churches",
        ]  # You can modify which fields you want to expose


# Serializer for the Transaction model
class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    church = serializers.PrimaryKeyRelatedField(queryset=Church.objects.all())

    class Meta:
        model = Transaction
        fields = ["amount", "user", "church", "date"]


class ChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = [
            "id",
            "name",
            "churchSize",
            "denomination",
        ]  # Include the fields you want to expose in the API
