# urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from PullpayBE import views  # Correct app import

router = DefaultRouter()
router.register(r"api/transactions", views.TransactionViewSet, basename="transaction")
router.register(r"api/users", views.UserViewSet, basename="user")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),  # Automatically includes all API routes
    path(
        "api/register/", views.register_user, name="register_user"
    ),  # Registration URL
]
