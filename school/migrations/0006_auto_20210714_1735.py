# Generated by Django 3.2 on 2021-07-14 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0005_alter_student_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.PositiveIntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four')], default=1),
        ),
        migrations.CreateModel(
            name='PickedUpDroppedOff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('parents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.guardian')),
                ('students', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
