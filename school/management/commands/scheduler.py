from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from school.models import *
from django.core.management.base import BaseCommand, CommandError


def clear_all():
    GuardiansLocation.objects.all().delete()
    GuardianPickupSpot.objects.all().delete()


def assign_spot():
    near_parents = GuardiansLocation.objects.all().order_by('guardian', '-timeStamp', 'distance').distinct('guardian')
    for obj in near_parents:
        if GuardianPickupSpot.objects.filter(guardian=obj.guardian).exists():
            print("Exist")
        else:
            spots = PickupSpot.objects.annotate(numbers_of_spot_occupied=Count('guardianpickupspot')).order_by(
                'numbers_of_spot_occupied')[0]
            GuardianPickupSpot(guardian=obj.guardian, pickup_spot=spots).save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        sched = BlockingScheduler()
        sched.add_job(clear_all, 'interval', hours=6)
        sched.add_job(assign_spot, 'interval', seconds=10)
        sched.start()
