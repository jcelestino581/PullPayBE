from rest_framework import serializers
from .models import User, Transaction, Church  # Import the models


# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "churches",
        ]  # You can modify which fields you want to expose


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["firstName", "lastName", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Ensure the password is hashed
        user.save()
        return user


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
