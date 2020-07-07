from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics
# Create your views here.


class HospitalList(generics.ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class HospitalRead(generics.RetrieveAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

