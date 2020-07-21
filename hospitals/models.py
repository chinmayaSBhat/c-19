from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class LocationEntity(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    logo = models.URLField(max_length=2500, null=True, blank=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    address = models.TextField(max_length=1500)
    pincode = models.CharField(max_length=6)
    phone_area_code = models.CharField(max_length=6)
    contact = models.CharField(max_length=10, unique=True)
    country_code = models.CharField(max_length=5, default="+91")
    active  = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        abstract = True

class Hospital(LocationEntity):
    total_isolation_beds = models.SmallIntegerField(default=0)
    total_icu_beds = models.SmallIntegerField(default=0)
    total_ventilated_beds = models.SmallIntegerField(default=0)
    total_high_oxygen_flow_beds = models.SmallIntegerField(default=0)
    total_regular_oxygen_flow_beds = models.SmallIntegerField(default=0)
    
    
class Patient(models.Model):
    name = models.CharField(max_length=500)
    contact = models.CharField(max_length=10, unique=True)
    country_code = models.CharField(max_length=5, default="+91")
    adhaar_number = models.CharField(max_length=12, null=True,blank=True)
    admitted_to = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    bed_type = models.CharField(max_length=50, choices=(
        ("ISOLATION","ISOLATION"),
        ("ICU","ICU"),
        ("VENTILATED","VENTILATED"),
        ("HIGH FLOW OXYGEN","HIGH FLOW OXYGEN"),
        ("REGULAR FLOW OXYGEN","REGULAR FLOW OXYGEN")
    ), default="ISOLATION")
    admission_timestamp = models.DateTimeField(auto_now=True)
    discharge_timestamp = models.DateTimeField(editable=False, null=True)
    discharged = models.BooleanField(default=False)
   
    def __str__(self):
        return str(self.name)
         

class Ambulance(LocationEntity):
    registration_number = models.CharField(max_length=20, unique=True)
    associated_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    logged_in = models.CharField(max_length=5, default="true", choices=(
    ("true","true"),
    ("false","false")
    ))
    occupied = models.CharField(max_length=5, default="false", choices=(
    ("true","true"),
    ("false","false")
    ))
    ambulance_type = models.CharField(max_length=20, choices=(
        ("ICU","ICU"),
        ("COLLECTIVE","COLLECTIVE"),
        ("LIFE SUPPORT","LIFE SUPPORT"),
        ("LCV","LCV")
    ))

    def __str__(self):
        return str(self.name) + " - " + str(self.registration_number)
    

class MedicalService(LocationEntity):
    occupied = models.BooleanField(default=False)
    associated_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    service_type = models.CharField(max_length=20,choices=(
        ("PHARMACY","PHARMACY"),
        ("LABORATORY","LABORATORY"),
        ("CLINIC","CLINIC")
    ))

    def __str__(self):
        return str(self.name)

