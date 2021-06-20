from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import viewsets
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from school.api.serializers import *
from school.api.logic import nearest_parents


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
def update_parents_location(request):
    if request.method == 'POST':
        print(request.data)
        data = {}
        timeStamp = 0
        try:
            timeStamp = int(request.data['timeStamp'])
            print(timeStamp)
        except Exception:
            print(Exception)
        pdata = {
            'latitude': request.data['latitude'],
            'longitude': request.data['longitude'],
            'timeStamp': datetime.fromtimestamp(int(request.data['timeStamp']) / 1000),
            'source_of_location': request.user.id,
        }
        serializers = GuardianLocationSerializers(data=pdata)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


