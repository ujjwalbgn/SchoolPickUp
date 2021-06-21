from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import viewsets
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from school.api.serializers import *
from school.api.logic import nearest_parents
import geopy.distance as calcualtedistance
from school.models import SchoolDetails


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


parentslocation = []


@api_view(['POST'])
def updateguardainLocation(request):
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
            'user': request.user.id,
        }
        # parentslocation.append(pdata)
        print(pdata)
        serializers = GuardianLocationSerializers(data=pdata)
        if serializers.is_valid():
            serializers.save()

            return Response(parentslocation, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# def UpdateUserLocation(APIView):
#     def post(self, request):
@api_view(['GET'])
def getnearbyParents(request):
    if request.method == 'GET':
        return JsonResponse(parentsDistance)


parentsDistance = {}


#
# @api_view(['POST'])
# def updateGurdainDistance(request):
#     getSchoolDetails = SchoolDetails.objects.first()
#     pDistance = calcualtedistance.distance((request.data['latitude'], request.data['longitude']),
#                                            (getSchoolDetails.latitude, getSchoolDetails.longitude)).m
#     if request.user.id in parentsDistance:
#         if pDistance < parentsDistance[request.user.id]:
#             parentsDistance[request.user.id] = pDistance
#     else:
#         parentsDistance[request.user.id] = pDistance
#     print(parentsDistance)
#     return JsonResponse(parentsDistance)


@api_view(['GET'])
def clear_location(request):
    GuardiansLocation.objects.all().delete()
    print(GuardiansLocation.objects.all())
    return JsonResponse({'cleared': 'cleared'})





