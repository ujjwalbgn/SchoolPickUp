# Generated by Django 3.2 on 2021-06-22 15:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_alter_student_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]
