from django.urls import path, include
from rest_framework.routers import DefaultRouter
from school.api import views

app_name = "school_api"

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'guardian', views.GuardianViewSet)
router.register(r'school_details', views.SchoolDetailsViewSet)
router.register(r'create_guardians_location', views.GuardiansLocationViewSet)
# router.register(r'updateParentsLocation', views.updateguardainLocation)


urlpatterns = [
    path('updateguardainLocation', views.updateguardainLocation, name="updategurdainLocation"),
    path('getnearbyParents', views.get_nearest_parents, name="getnearbyparents"),
    path('updatePickUpDropOff', views.updatePickUpDropOff, name="updatePickUpDropOff"),
    path('clear_location', views.clear_location, name='clearLocation'),
    path('', include(router.urls)),
    path('clear_pickUpDropOff', views.clear_pickUpDropOff, name='clear_pickUpDropOff'),


]
