from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from school.models import *
from school.api.serializers import *


# Create your views here.

# @api_view(['GET'])
# def api_root(request, format=None):
# return Response({
#     'guardian': reverse('guardian-list', request=request, format=format),
# })


# TODO make it available only for staff
class GuardianViewSet(viewsets.ReadOnlyModelViewSet):
    #
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializers


class SchoolDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolDetails.objects.all()
    serializer_class = SchoolDetailsSerializers


# TODO make get list available only for staff
class GuardiansLocationViewSet(viewsets.ModelViewSet):
    serializer_class = GuardianLocationSerializers
    queryset = GuardiansLocation.objects.all()


@api_view(['POST'])
def updateguardainLocation(request):
    if request.method == 'POST':

        print(request.data)
        data={}
        timeStamp = 0
        try:
            timeStamp= int(request.data['timeStamp'])
            print(timeStamp)
        except Exception:
            print(Exception)
        pdata = {
            'latitude': request.data['latitude'],
            'longitude': request.data['longitude'],
            'timeStamp': datetime.fromtimestamp(int(request.data['timeStamp'])/1000),
            'source_of_location': request.user.id,
        }
        print(request.data)
        serializers = GuardianLocationSerializers(data=pdata)
        if serializers.is_valid():
            print('OKAY')
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)


        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# def UpdateUserLocation(APIView):
#     def post(self, request):
