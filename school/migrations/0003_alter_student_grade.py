# Generated by Django 3.2 on 2021-06-22 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_student_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.IntegerField(default=1),
        ),
    ]
