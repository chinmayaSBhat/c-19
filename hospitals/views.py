from django.shortcuts import get_object_or_404, render
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.generic import ListView, DetailView

# Create your views here.

class ArundhathiLocationView(APIView):
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


class HospitalList(ArundhathiLocationView):
    def __obtain_queryset__(self):
        return Hospital.objects.all()
    
    def __obtain_serializer__(self):
        return HospitalSerializer
    
class AmbulanceList(ArundhathiLocationView):
    def __obtain_queryset__(self):
        return Ambulance.objects.all()

    def __obtain_serializer__(self):
        return AmbulanceSerializer


class AmbulanceDetail(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Ambulance.objects.filter(admin=user)
    
    serializer_class = AmbulanceMinimalSerializer


class AmbulanceUpdate(APIView):
    
    def post(self, request, format=None):
        ambulance_id = request.data["id"]
        occupied = request.data["occupied"]
        user_longitude = request.data["longitude"]
        user_latitude = request.data["latitude"]
        
        context_ambulance = Ambulance.objects.get(id=ambulance_id)
        
        context_ambulance.occupied = occupied
        context_ambulance.latitude = user_latitude
        context_ambulance.longitude = user_longitude
        
        context_ambulance.save()
        
        serialized = AmbulanceMinimalSerializer(context_ambulance, many=False)
        
        return Response(serialized.data)
  

class MedicalServiceList(ArundhathiLocationView):
    def __obtain_queryset__(self):
        return MedicalService.objects.all()

    def __obtain_serializer__(self):
        return MedicalSerivceSerializer    


class PatientListView(ListView):
    model = Patient
    context_object_name = "patient_list"

    def get_queryset(self):
        context_hospital = get_object_or_404(Hospital, admin=self.request.user)
        context_patient_list = Patient.objects.filter(admitted_to= context_hospital)
        return context_patient_list


class PatientReadView(DetailView):
    model  = Patient
    context_object_name = "patient_detail"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investigations'] = Investigation.objects.filter(patient = self.get_object())
        context['observations'] = Observation.objects.filter(patient = self.get_object())
        return context