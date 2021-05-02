# This url.py is added to SchoolPickup_backend.urls.py

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from accounts.api.views import(
    registration_view,
)

app_name = "accounts"

urlpatterns = [
    # This will return a token when user login
    path('login', obtain_auth_token, name='api-login'),

    #  This will allow user registration using API requests
    # path('register', registration_view, name="api-register"),

]