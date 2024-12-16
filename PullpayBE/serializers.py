from rest_framework import serializers
from .models import User, Transaction, Church  # Import the models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "churches"]
        depth = 1  # Expand related fields like churches if necessary


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


class TransactionSerializer(serializers.ModelSerializer):
    # Adding user's first name and last name to the transaction serializer
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    user_last_name = serializers.CharField(source="user.last_name", read_only=True)
    church_name = serializers.CharField(
        source="church.name"
    )  # Add this line to include church name

    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "date",
            "user",
            "church",
            "user_first_name",
            "user_last_name",
            "church_name",
        ]


class ChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Use the built-in User model
        fields = [
            "first_name",
            "last_name",
            "email",
        ]  # Include the fields you want to update

    def update(self, instance, validated_data):
        # Here we manually update the fields of the `User` model
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)

        instance.save()
        return instance
