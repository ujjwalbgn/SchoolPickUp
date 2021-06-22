from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets, status, authentication, permissions, generics
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime
from school.api.serializers import *
from school.models import SchoolDetails
from django.core import serializers
from django.core.serializers.json import Serializer, DjangoJSONEncoder


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


# @api_view(['GET'])
# def getnearbyParents(request):
#     if request.method == 'GET':
#         if request.user.is_staff:
#             NearestParents.

@api_view(['GET'])
def clear_location(request):
    GuardiansLocation.objects.all().delete()
    NearestParents.objects.all().delete()
    print(GuardiansLocation.objects.all())
    return JsonResponse({'cleared': 'cleared'})


@api_view(['GET'])
def get_nearest_parents(request):
    near_parents = NearestParents.objects.order_by('distance')
    near_parents_response = {}
    for obj in near_parents:
        try:
            get_parents_info = Guardian.objects.filter(user=obj.user)[0]
            if get_parents_info:
                parents_json = ParentsSerializer(get_parents_info).data
                print(request.data)
                if request.data['grade'] == '0':
                    student_info = Student.objects.filter(studentandguardian__Guardian=get_parents_info)

                else:
                    student_info = Student.objects.filter(studentandguardian__Guardian=get_parents_info,
                                                          grade=int(request.data['grade']))

                childrens = {}
                if len(student_info):
                    for stud_obj in student_info:
                        student_data = StudentSerializer(stud_obj).data
                        childrens[str(student_data['id'])] = student_data
                    parents_json["children"] = childrens
                    near_parents_response[str(parents_json["user"])] = parents_json
                print(near_parents_response)

        except Exception:
            return Response(status=500)

    return Response(near_parents_response)
