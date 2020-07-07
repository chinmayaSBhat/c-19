from rest_framework import serializers
from .models import *
from django.db.models import Count

class HospitalSerializer(serializers.ModelSerializer):
    remaining_beds = serializers.SerializerMethodField("get_remaining_beds")

    def get_remaining_beds(self, obj):
        return obj.total_beds - Patient.objects.filter(admitted_to=obj, discharged=False).count()

    class Meta:
        model = Hospital
        fields = ["name","longitude", "latitude", "total_beds","address","pincode","phone_area_code","contact","country_code", "remaining_beds"]