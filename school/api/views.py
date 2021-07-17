from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime, timedelta
from school.api.serializers import *
from school.models import SchoolDetails
from django.utils import timezone
import geopy.distance as calculate_distance


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
        getSchoolDetails = SchoolDetails.objects.first()
        pdata = {
            'latitude': request.data['latitude'],
            'longitude': request.data['longitude'],
            # 'timeStamp': datetime.fromtimestamp(int(request.data['timeStamp']) / 1000),
            'timeStamp': timezone.now(),
            'user': request.user.id,
            'distance': round(calculate_distance.distance((request.data['latitude'], request.data['longitude']),
                                                          (getSchoolDetails.latitude, getSchoolDetails.longitude)).m, 5)
        }
        # parentslocation.append(pdata)
        print(pdata)
        serializers = GuardianLocationSerializers(data=pdata)

        if serializers.is_valid():
            serializers.save()
            return Response(parentslocation, status=status.HTTP_201_CREATED)
        else:

            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def clear_location(request):
    GuardiansLocation.objects.all().delete()
    NearestParents.objects.all().delete()
    print(GuardiansLocation.objects.all())
    return JsonResponse({'cleared': 'cleared'})


@api_view(['GET'])
def get_nearest_parents(request):
    near_parents = GuardiansLocation.objects.all().filter(
        timeStamp__range=((timezone.now() - timedelta(hours=6)), timezone.now())).order_by('user', '-timeStamp',
                                                                                           'distance').distinct(
        'user')
    near_parents_response = []
    picked_student = PickedUpDroppedOff.objects.filter(
        timestamp__range=((timezone.now() - timedelta(hours=6)), timezone.now())).values_list('students')
    requested_grade = request.GET['grade']
    for obj in near_parents:
        try:
            get_parents_info = Guardian.objects.filter(user=obj.user)[0]
            if get_parents_info:
                parents_json = ParentsSerializer(get_parents_info).data
                parents_json["distance"] = obj.distance
                if requested_grade == "ALL":
                    student_info = Student.objects.filter(studentandguardian__Guardian=get_parents_info).exclude(
                        id__in=picked_student)
                else:
                    student_info = Student.objects.filter(studentandguardian__Guardian=get_parents_info,
                                                          grade=int(requested_grade)).exclude(
                        id__in=picked_student)
                children = []
                if len(student_info):
                    for stud_obj in student_info:
                        student_data = StudentSerializer(stud_obj).data
                        children.append(student_data)
                    parents_json["children"] = children
                    near_parents_response.append(parents_json)
                # print(near_parents_response)
        except Exception:
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

        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def clear_pickUpDropOff(request):
    PickedUpDroppedOff.objects.all().delete()
    return JsonResponse({'cleared': 'cleared'})
