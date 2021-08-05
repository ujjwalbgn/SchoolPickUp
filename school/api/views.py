from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime, timedelta
from school.api.serializers import *
from school.models import SchoolDetails
from django.utils import timezone
import geopy.distance as calculate_distance


# helper Function

def check_if_student_picked_dropped(request):
    picked_student = PickedUpDroppedOff.objects.filter(
        timestamp__range=((timezone.now() - timedelta(hours=6)), timezone.now())).values_list('students')
    get_parents_info = Guardian.objects.filter(user=request.user.id)[0]
    student_info = Student.objects.filter(studentandguardian__Guardian=get_parents_info).exclude(id__in=picked_student)
    if len(student_info):
        return False
    else:
        return True


def get_locationSpot(id):
    get_guard = Guardian.objects.filter(user=id)[0]
    if GuardianPickupSpot.objects.filter(guardian=get_guard).exists():
        return GuardianPickupSpotSerializer(
            GuardianPickupSpot.objects.filter(guardian=get_guard)[0]).data
    else:
        return {}


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
        if check_if_student_picked_dropped(request):
            return JsonResponse({'picked': 'true'})
        getSchoolDetails = SchoolDetails.objects.first()
        obj = Guardian.objects.filter(user=request.user.id)[0]
        pdata = {
            'latitude': request.data['latitude'],
            'longitude': request.data['longitude'],
            'timeStamp': timezone.now(),
            'guardian': obj.id,
            'distance': round(calculate_distance.distance((request.data['latitude'], request.data['longitude']),
                                                          (getSchoolDetails.latitude, getSchoolDetails.longitude)).m, 5)
        }
        # parentslocation.append(pdata)
        serializers = GuardianLocationSerializers(data=pdata)
        if serializers.is_valid():
            serializers.save()
            response = {'picked': 'false'}
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            print(serializers.errors)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def clear_location(request):
    GuardiansLocation.objects.all().delete()

    print(GuardiansLocation.objects.all())
    return JsonResponse({'cleared': 'cleared'})


@api_view(['GET'])
def get_nearest_parents(request):
    near_parents = GuardiansLocation.objects.all().filter(
        timeStamp__range=((timezone.now() - timedelta(hours=6)), timezone.now())).order_by('guardian', '-timeStamp',
                                                                                           'distance').distinct(
        'guardian')
    near_parents_response = []
    picked_student = PickedUpDroppedOff.objects.filter(
        timestamp__range=((timezone.now() - timedelta(hours=6)), timezone.now())).values_list('students')
    requested_grade = request.GET['grade']
    for obj in near_parents:
        try:
            if requested_grade == "ALL":
                student_info = Student.objects.filter(studentandguardian__Guardian=obj.guardian).exclude(
                    id__in=picked_student)
            else:
                student_info = Student.objects.filter(studentandguardian__Guardian=obj.guardian,
                                                      grade=int(requested_grade)).exclude(
                    id__in=picked_student)
            children = []
            if len(student_info):

                parents_json = GuardianSerializers(obj.guardian).data
                parents_json["distance"] = obj.distance
                for stud_obj in student_info:
                    student_data = StudentSerializer(stud_obj).data
                    children.append(student_data)
                parents_json["children"] = children
                near_parents_response.append(parents_json)
                if GuardianPickupSpot.objects.filter(guardian=obj.guardian).exists():
                    parents_json["spot"] = GuardianPickupSpotSerializer(
                        GuardianPickupSpot.objects.filter(guardian=obj.guardian)[0]).data
                else:
                    parents_json["spot"] = {}
        except Exception:
            print(Exception)
            return Response(status=500)
    if near_parents_response:
        near_parents_response = sorted(near_parents_response, key=lambda obj: obj['distance'])
    return Response(near_parents_response)


@api_view(['POST'])
def update_pickup_drop_off(request):
    if request.method == 'POST':
        children = request.data['ids']
        if len(children) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for obj in children:
            pdata = {
                'parents': request.data['parent'],
                'students': obj,
                'timestamp': datetime.now(),
            }
            serializers = PickedUpDroppedOffSerializer(data=pdata)
            if serializers.is_valid():
                serializers.save()
            else:
                print(serializers.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)

        picked_student = PickedUpDroppedOff.objects.filter(
            timestamp__range=((timezone.now() - timedelta(hours=6)), timezone.now())).values_list('students')
        student_info = Student.objects.filter(studentandguardian__Guardian=request.data['parent']).exclude(
            id__in=picked_student)
        if len(student_info) == 0:
            GuardianPickupSpot.objects.filter(id=request.data['spot']).delete()
            # print(request.data)

        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def clear_pickUpDropOff(request):
    PickedUpDroppedOff.objects.all().delete()
    return JsonResponse({'cleared': 'cleared'})

@api_view(['GET','POST'])
def get_update_pickup_spot(request):
    if request.method == 'GET':
        response = {'spot': get_locationSpot(request.user.id)}
        return Response(response,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        return Response(status=status.HTTP_200_OK)
