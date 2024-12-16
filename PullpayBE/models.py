from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(first_name, last_name, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, blank=True, null=True
    )  # Ensure username is blank and nullable
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(
        unique=True, blank=False
    )  # Make email mandatory and unique
    churches = models.ManyToManyField(
        "Church", related_name="members", blank=True
    )  # Removed null=True as it's unnecessary for ManyToManyField
    objects = UserManager()

    # Add related_name to avoid clashes with default User model's groups and user_permissions
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",  # Custom related_name for groups
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",  # Custom related_name for user_permissions
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Use email for authentication instead of username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",  # Corrected to snake_case
        "last_name",  # Corrected to snake_case
    ]  # List other fields required for superuser


class Church(models.Model):

    CATHOLIC = "CA"
    BAPTIST = "BA"
    METHODIST = "ME"
    PENTECOSTAL = "PE"
    NON_DENOMINATIONAL = "ND"
    LUTHERAN = "LU"
    PRESBYTERIAN = "PR"
    ORTHODOX = "OR"

    DENOMINATION_CHOICES = {
        CATHOLIC: "Catholic",
        BAPTIST: "Baptist",
        METHODIST: "Methodist",
        PENTECOSTAL: "Pentecostal",
        NON_DENOMINATIONAL: "Non-Denominational",
        LUTHERAN: "Lutheran",
        PRESBYTERIAN: "Presbyterian",
        ORTHODOX: "Orthodox",
    }
    name = models.CharField(max_length=50)
    churchSize = models.PositiveIntegerField()
    denomination = models.CharField(
        max_length=2,
        choices=DENOMINATION_CHOICES.items(),  # Use items() for key-value pairs
        default=NON_DENOMINATIONAL,  # Default value
    )

    def __str__(self):
        return self.name


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    church = models.ForeignKey(
        Church, on_delete=models.CASCADE, default=1
    )  # Set default to an existing church ID
    date = models.DateTimeField(default=timezone.now)

# hello there testing