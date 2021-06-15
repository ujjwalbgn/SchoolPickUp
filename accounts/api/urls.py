# This url.py is added to SchoolPickup_backend.urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.api.views import(
    registration_view,
    CustomAuthToken,
    current_user,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()


app_name = "accounts_api"

urlpatterns = (
    # This will return a token when user login
    path('', include(router.urls)),
    path('login', CustomAuthToken.as_view(), name='api-login'),
    path('current_user', current_user,name='current-user')
    #  This will allow user registration using api requests
    # path('register', registration_view, name="api-register"),

)