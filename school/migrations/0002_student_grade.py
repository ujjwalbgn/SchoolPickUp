# Generated by Django 3.2 on 2021-06-22 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='grade',
            field=models.IntegerField(default=1, max_length=2),
        ),
    ]
