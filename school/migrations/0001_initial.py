# Generated by Django 3.2 on 2021-08-04 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=64)),
                ('last_name', models.CharField(default='', max_length=64)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('address_1', models.CharField(blank=True, max_length=128)),
                ('address_2', models.CharField(blank=True, max_length=128)),
                ('city', models.CharField(blank=True, default='', max_length=64)),
                ('state', models.CharField(blank=True, choices=[('AL', 'Alababama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('zip_code', models.CharField(blank=True, max_length=5)),
                ('phone_number', models.CharField(blank=True, max_length=128)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PickupSpot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_spot', models.CharField(max_length=128)),
                ('notes', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=10, max_digits=25)),
                ('longitude', models.DecimalField(decimal_places=10, max_digits=25)),
                ('geofencing_radius', models.DecimalField(decimal_places=5, default=0, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('student_id', models.CharField(blank=True, max_length=10)),
                ('grade', models.PositiveIntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four')], default=1)),
                ('address_1', models.CharField(blank=True, max_length=128)),
                ('address_2', models.CharField(blank=True, max_length=128)),
                ('city', models.CharField(blank=True, default='', max_length=64)),
                ('state', models.CharField(blank=True, choices=[('AL', 'Alababama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('zip_code', models.CharField(blank=True, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAndGuardian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Guardian', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.guardian')),
                ('relation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.relation')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='PickedUpDroppedOff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('parents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.guardian')),
                ('students', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='GuardiansLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=20, max_digits=25)),
                ('longitude', models.DecimalField(decimal_places=20, max_digits=25)),
                ('timeStamp', models.DateTimeField()),
                ('distance', models.DecimalField(decimal_places=5, max_digits=15)),
                ('guardian', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.guardian')),
            ],
        ),
        migrations.CreateModel(
            name='GuardianPickupSpot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guardian', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='school.guardian')),
                ('pickup_spot', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='school.pickupspot')),
            ],
        ),
    ]
