from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class AhalyaLocationView(APIView):
    def __obtain_queryset__(self):
        return Hospital.objects.all()
    
    def __obtain_serializer__(self):
        return HospitalSerializer

    def post(self, request, format=None):
        
        user_longitude = request.data["longitude"]
        user_latitude = request.data["latitude"]
        queryset = __obtain_queryset__(self)
        serializer = __obtain_serializer__(self)         
        serialized = serializer(queryset, many=True,
        context={"user_longitude":user_longitude, "user_latitude":user_latitude}
        )

        return Response(serialized.data)


class HospitalDetailedList(AhalyaLocationView):
    def __obtain_queryset__(self):
        return Hospital.objects.all()
    
    def __obtain_serializer__(self):
        return HospitalSerializer
    
class AmbulanceDetailedList(AhalyaLocationView):
    def __obtain_queryset__(self):
        return Ambulance.objects.all()

    def __obtain_serializer__(self):
        return AmbulanceSerializer

class MedicalServiceDetailedList(AhalyaLocationView):
    def __obtain_queryset__(self):
        return MedicalService.objects.all()

    def __obtain_serializer__(self):
        return MedicalSerivceSerializer    