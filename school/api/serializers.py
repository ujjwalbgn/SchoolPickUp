from rest_framework import serializers

# Todo need to only import used classes
from school.models import *

from accounts.models import SchoolUser


class GuardianSerializers(serializers.HyperlinkedModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    url = serializers.HyperlinkedIdentityField(view_name="school_api:guardian-detail")

    class Meta:
        model = Guardian
        fields = ['url','user_email', 'first_name', 'last_name', 'phone_number']

#
