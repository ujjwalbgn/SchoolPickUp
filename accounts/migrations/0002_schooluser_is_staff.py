# Generated by Django 3.2 on 2021-06-10 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schooluser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
