from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class AhalyaLocationView(APIView):
    def __obtain_queryset__(self):
        pass
    
    def __obtain_serializer__(self):
        pass

    def post(self, request, format=None):
        
        user_longitude = request.data["longitude"]
        user_latitude = request.data["latitude"]
        queryset = self.__obtain_queryset__()
        serializer = self.__obtain_serializer__()         
        serialized = serializer(queryset, many=True,
        context={"user_longitude":user_longitude, "user_latitude":user_latitude}
        )

        return Response(serialized.data)


class HospitalList(AhalyaLocationView):
    def __obtain_queryset__(self):
        return Hospital.objects.all()
    
    def __obtain_serializer__(self):
        return HospitalSerializer
    
class AmbulanceList(AhalyaLocationView):
    def __obtain_queryset__(self):
        return Ambulance.objects.all()

    def __obtain_serializer__(self):
        return AmbulanceSerializer


class AmbulanceDetail(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Ambulance.objects.filter(admin=user)
    
    serializer_class = AmbulanceSerializer


class AmbulanceUpdate(generics.UpdateAPIView):
    
    permission_classes = [IsAuthenticated]

    queryset = Ambulance.objects.all()
    
    serializer_class = AmbulanceMinimalSerializer



class MedicalServiceList(AhalyaLocationView):
    def __obtain_queryset__(self):
        return MedicalService.objects.all()

    def __obtain_serializer__(self):
        return MedicalSerivceSerializer    
