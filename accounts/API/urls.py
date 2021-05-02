# This url.py is added to SchoolPickup_backend.urls.py

from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

app_name = "accounts"

urlpatterns = [
    # this will return a token when user login
    path('login', obtain_auth_token, name='api-login')

]