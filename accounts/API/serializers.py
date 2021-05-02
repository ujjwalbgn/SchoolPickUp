from rest_framework import serializers
from accounts.models import SchoolUser

class SchoolUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = SchoolUser
        fields = ('id','email')