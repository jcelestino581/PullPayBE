# urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from PullpayBE import views  # Ensure the correct app import
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/login/", views.LoginView.as_view(), name="login"),
    path("api/user/", views.UserDetailView.as_view(), name="user-detail"),
    path("api/user/", views.get_profile, name="get_profile"),  # Handle GET requests
    path(
        "api/user/", views.update_profile, name="update_profile"
    ),  # Handle PUT requests
    path(
        "api/user/", views.UserProfileView.as_view(), name="user_profile"
    ),  # Use ProfileView for both GET and PUT
    path("user/", views.UserProfileView.as_view(), name="user-profile"),
]
