# urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from PullpayBE import views  # Ensure the correct app import
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt import views as jwt_views

# from .views import update_profile


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/login/", views.LoginView.as_view(), name="login"),
    path("api/user/", views.UserDetailView.as_view(), name="user-detail"),
    path("api/user/", views.get_profile, name="get_profile"),  # Handle GET requests
    # path("user/", views.update_profile, name="update_profile"),
    path("user/", views.user_profile, name="user"),  # Ensure this is correct
]
