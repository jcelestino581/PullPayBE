from django.db import models
import uuid
from django.utils import timezone

# Create your models here.


class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    churches = models.ManyToManyField("Church", related_name="members")

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


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
