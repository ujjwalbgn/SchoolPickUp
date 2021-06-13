from django.urls import path, include
from rest_framework.routers import DefaultRouter
from school.api import views

app_name = "school_api"

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'guardian',views.GuardianViewSet)
router.register(r'school_details',views.SchoolDetailsViewSet)
router.register(r'create_guardians_location',views.GuardiansLocationViewSet)


urlpatterns = [
    path('', include(router.urls)),

]
