from django.contrib import admin
from .models import Transaction, User, Church

# Register your models here.
admin.site.register(Transaction)
admin.site.register(User)
admin.site.register(Church)

