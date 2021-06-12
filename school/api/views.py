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

from rest_framework.decorators import action
from rest_framework.response import Response

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
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializers

# class