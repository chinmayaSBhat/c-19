from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.db.models import Count

from geopy.distance import geodesic



class HospitalMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = "__all__"

class UserMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

class AmbulanceMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ambulance
        fields = "__all__"

class HospitalSerializer(serializers.ModelSerializer):
    remaining_isolation_beds = serializers.SerializerMethodField("get_remaining_isolation_beds")
    remaining_icu_beds = serializers.SerializerMethodField("get_remaining_icu_beds")
    remaining_ventilated_beds  = serializers.SerializerMethodField("get_remaining_ventilated_beds")
    remaining_high_oxygen_flow_beds = serializers.SerializerMethodField("get_remaining_high_oxygen_flow_beds")
    remaining_regular_oxygen_flow_beds = serializers.SerializerMethodField("get_remaining_regular_oxygen_flow")
    geodesic_distance = serializers.SerializerMethodField("get_distance")
    bed_availability = serializers.SerializerMethodField("get_availability")
    comfortness = serializers.SerializerMethodField("get_comfortness")
    

    def get_remaining_isolation_beds(self, obj):
        return obj.total_isolation_beds - Patient.objects.filter(admitted_to=obj, bed_type="ISOLATION" ,discharged=False).count()

    def get_remaining_icu_beds(self, obj):
        return obj.total_icu_beds - Patient.objects.filter(admitted_to=obj,bed_type="ICU", discharged=False).count()

    def get_remaining_ventilated_beds(self, obj):
        return obj.total_ventilated_beds - Patient.objects.filter(admitted_to=obj, bed_type="VENTILATED" ,discharged=False).count()

    def get_remaining_high_oxygen_flow_beds(self, obj):
        return obj.total_high_oxygen_flow_beds - Patient.objects.filter(admitted_to=obj, bed_type="HIGH FLOW OXYGEN" ,discharged=False).count()            

    def get_remaining_regular_oxygen_flow(self, obj):
        return obj.total_regular_oxygen_flow_beds - Patient.objects.filter(admitted_to=obj, bed_type="REGULAR FLOW OXYGEN" ,discharged=False).count()

    def get_distance(self, obj):
        user_longitude = self.context.get("user_longitude")
        user_latitude = self.context.get("user_latitude")

        return round(geodesic((user_longitude, user_latitude), (obj.longitude, obj.latitude)).kilometers,2)

    def get_availability(self, obj):
        total_beds = (obj.total_isolation_beds+ 
        obj.total_icu_beds+ obj.total_ventilated_beds+ obj.total_high_oxygen_flow_beds
        + obj.total_regular_oxygen_flow_beds)
        remaining_beds = total_beds - Patient.objects.filter(admitted_to=obj, discharged=False).count()
        return {"total_beds":total_beds,"remaining_beds":remaining_beds,"bed_availability":int((remaining_beds/total_beds)*100)}

    
    
    def get_comfortness(self, obj):
        total_beds = (obj.total_isolation_beds+ 
        obj.total_icu_beds+ obj.total_ventilated_beds+ obj.total_high_oxygen_flow_beds
        + obj.total_regular_oxygen_flow_beds)
        remaining_beds = total_beds - Patient.objects.filter(admitted_to=obj, discharged=False).count()
        availability = int((remaining_beds/total_beds)*100)
        user_longitude = self.context.get("user_longitude")
        user_latitude = self.context.get("user_latitude")

        distance = geodesic((user_longitude, user_latitude), (obj.longitude, obj.latitude)).miles
        
        comfortness = availability//distance

        return comfortness

    class Meta:
        model = Hospital
        fields = ["id","name", "logo","longitude", "latitude","address",
        "pincode","phone_area_code","contact","country_code","active",
        "total_isolation_beds","total_icu_beds","total_ventilated_beds","total_high_oxygen_flow_beds","total_regular_oxygen_flow_beds", 
        "remaining_isolation_beds","remaining_icu_beds","remaining_ventilated_beds","remaining_high_oxygen_flow_beds","remaining_regular_oxygen_flow_beds",
        "geodesic_distance","comfortness","bed_availability"]


class AmbulanceSerializer(serializers.ModelSerializer):
    associated_hospital = HospitalMinimalSerializer(many=False)
    admin = UserMinimalSerializer(many=False)
    geodesic_distance = serializers.SerializerMethodField("get_distance")
    def get_distance(self, obj):
        user_longitude = self.context.get("user_longitude")
        user_latitude = self.context.get("user_latitude")

        return round(geodesic((user_longitude, user_latitude), (obj.longitude, obj.latitude)).kilometers,2)

    class Meta:
        model = Ambulance
        fields = ["id","name", "logo","longitude", "latitude","address",
        "pincode","phone_area_code","contact","country_code","admin","active","registration_number","associated_hospital","logged_in","occupied","ambulance_type",
        "geodesic_distance"]

class MedicalSerivceSerializer(serializers.ModelSerializer):
    geodesic_distance = serializers.SerializerMethodField("get_distance")
    def get_distance(self, obj):
        user_longitude = self.context.get("user_longitude")
        user_latitude = self.context.get("user_latitude")

        return round(geodesic((user_longitude, user_latitude), (obj.longitude, obj.latitude)).kilometers,2)

    class Meta:
        model = MedicalService
        fields = ["id","name", "logo","longitude", "latitude","address",
        "pincode","phone_area_code","contact","country_code","active","associated_hospital","occupied","service_type",
        "geodesic_distance"]

