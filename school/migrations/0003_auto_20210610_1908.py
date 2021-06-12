# Generated by Django 3.2 on 2021-06-11 00:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0002_guardianslocation_schooldetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guardianslocation',
            name='source',
        ),
        migrations.AddField(
            model_name='guardianslocation',
            name='source_of_location',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]