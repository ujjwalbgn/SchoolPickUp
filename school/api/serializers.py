from rest_framework import serializers
from django.contrib.auth.models import User

# Todo need to only import used classes
from school.models import *

class GuardianDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = '__all__'


