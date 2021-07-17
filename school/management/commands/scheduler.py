from apscheduler.schedulers.blocking import BlockingScheduler
from school.models import GuardiansLocation, SchoolDetails, NearestParents
from django.core.management.base import BaseCommand, CommandError


def clear_location():
    GuardiansLocation.objects.all().delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        sched = BlockingScheduler()
        sched.add_job(clear_location, 'interval', hours=12)
        sched.start()
