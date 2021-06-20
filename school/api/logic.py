from school.models import GuardiansLocation
import geopy.distance as calcualtedistance
from school.models import SchoolDetails


def nearest_parents():
    getallobject = GuardiansLocation.objects.all().order_by('user', '-timeStamp').distinct(
        'user')
    getschooldetails = SchoolDetails.objects.first()
    nearbyparents = {}
    for obj in getallobject:
        pdistance = calcualtedistance.distance((obj.latitude, obj.longitude),
                                               (getschooldetails.latitude, getschooldetails.longitude)).m
        nearbyparents.update()