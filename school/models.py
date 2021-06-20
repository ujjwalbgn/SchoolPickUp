from django.db import models
from accounts.models import SchoolUser


# Create your models here.

class Student(models.Model):
    US_STATES = [('AL', 'Alababama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
                 ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'),
                 ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'),
                 ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'),
                 ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'),
                 ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
                 ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
                 ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
                 ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
                 ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'),
                 ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    student_id = models.CharField(max_length=10, blank=True)

    address_1 = models.CharField(max_length=128, blank=True)
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, default="", blank=True)
    state = models.CharField(max_length=2, choices=US_STATES, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)

    def __str__(self):
        display = (self.first_name + " " + self.last_name)
        return display


class Relation(models.Model):
    relation = models.CharField(max_length=100)

    def __str__(self):
        return self.relation


class Guardian(models.Model):
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, blank=True, null=True)

    first_name = models.CharField(max_length=64, default="")
    last_name = models.CharField(max_length=64, default="")
    date_of_birth = models.DateField(null=True, blank=True)

    US_STATES = [('AL', 'Alababama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
                 ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'),
                 ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'),
                 ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'),
                 ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'),
                 ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
                 ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
                 ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
                 ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
                 ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'),
                 ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]

    address_1 = models.CharField(max_length=128, blank=True)
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, default="", blank=True)
    state = models.CharField(max_length=2, choices=US_STATES, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)

    phone_number = models.CharField(max_length=128, blank=True)

    def __str__(self):
        display = (self.first_name + " " + self.last_name)
        return display


class StudentAndGuardian(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    Guardian = models.ForeignKey(Guardian, on_delete=models.PROTECT)
    relation = models.ForeignKey(Relation, on_delete=models.PROTECT)

    def __str__(self):
        display = ("Student Name: " + str(self.student) + " Guardian Name: " + str(self.Guardian))
        return display


class SchoolDetails(models.Model):
    latitude = models.DecimalField(null=False, max_digits=25, decimal_places=10)
    longitude = models.DecimalField(null=False, max_digits=25, decimal_places=10)
    geofencing_radius = models.DecimalField(null=False, max_digits=20, decimal_places=5, default=0)


class GuardiansLocation(models.Model):
    source_of_location = models.ForeignKey(SchoolUser, on_delete=models.PROTECT)
    latitude = models.DecimalField(null=False, max_digits=25, decimal_places=20)
    longitude = models.DecimalField(null=False, max_digits=25, decimal_places=20)
    timeStamp = models.DateTimeField(null=False)

    def __str__(self):
        display = (str(self.source_of_location.get_username()) + "  " + str(self.timeStamp))
        return display


class NearestParents(models.Model):
    parents = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, primary_key=True)
    distance = models.DecimalField(null=False, max_digits=15, decimal_places=5)

    def __str__(self):
        display = (str(self.parents.get_username()) + "  Distance:  " + str(self.distance) + "m")
        return display
