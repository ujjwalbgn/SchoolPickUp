from apscheduler.schedulers.blocking import BlockingScheduler
from school.models import GuardiansLocation, SchoolDetails, NearestParents
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime, timedelta
import geopy.distance as calcualtedistance


def clear_location():
    GuardiansLocation.objects.all().delete()


def update_parents_distance():
    getSchoolDetails = SchoolDetails.objects.first()
    getallobject = GuardiansLocation.objects.all().order_by('user', '-timeStamp').distinct(
        'user').filter( timeStamp__range=((timezone.now() - timedelta(hours=6)), timezone.now()))
    print(getallobject)
    for obj in getallobject:
        pdistance = calcualtedistance.distance((obj.latitude, obj.longitude),
                                               (getSchoolDetails.latitude, getSchoolDetails.longitude)).m
        if NearestParents.objects.filter(user=obj.user).exists():
            parents = NearestParents.objects.get(user=obj.user)
            parents.distance = pdistance
            parents.save()
        else:
            parents = NearestParents(user=obj.user, distance=pdistance)
            parents.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        sched = BlockingScheduler()
        sched.add_job(update_parents_distance, 'interval', seconds=5)
        sched.add_job(clear_location, 'interval', hours=12)
        sched.start()

