from rest_framework import serializers
from django.contrib.auth.models import User

# Todo need to only import used classes
from school.models import *

from accounts.models import SchoolUser

class GuardianDetailsSerializers(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Guardian
        fields = ['user_email','first_name','last_name']


#