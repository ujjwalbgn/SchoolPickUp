from apscheduler.schedulers.blocking import BlockingScheduler
from school.models import GuardiansLocation, SchoolDetails, NearestParents
from django.core.management.base import BaseCommand, CommandError

import geopy.distance as calcualtedistance


def clear_location():
    GuardiansLocation.objects.all().delete()


def update_parents_distance():
    get_school_details = SchoolDetails.objects.first()
    get_all_objects = GuardiansLocation.objects.all().order_by('user', '-timeStamp').distinct(
        'user')
    for obj in get_all_objects:
        p_distance = calcualtedistance.distance((obj.latitude, obj.longitude),
                                               (get_school_details.latitude, get_school_details.longitude)).m
        if NearestParents.objects.filter(parents=obj.user).exists():
            parents = NearestParents.objects.get(parents=obj.user)
            parents.distance = p_distance
            parents.save()
        else:
            parents = NearestParents(parents=obj.user, distance=p_distance)
            parents.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        sched = BlockingScheduler()
        sched.add_job(update_parents_distance, 'interval', seconds=5)

        sched.start()
