from django.db import models
from django.contrib.auth.models import User, User
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError
# Create your models here.

def validate_department(self, obj):
    if hasattr(obj, "observationn_for"):
        if obj.observation_for.authorised_department is obj.observing_doctor.department:
            if obj.patient.admitted_to is obj.observing_doctor.department.hospital:
                return True
    
    elif hasattr(obj, "investigation_for"):
        if obj.patient.admitted_to is obj.investigating_doctor.department.hospital:
            return True
    
    raise ValidationError("Only doctors belonging to same hospital and authorised department can do the test!")


class ServiceEntity(models.Model):
    service_type = models.CharField(max_length = 100)
    icon_url = models.URLField(max_length=2000, null=True, blank=True)
    description = models.TextField(max_length = 200, null=True, blank=True)
    
    def __str__(self):
        return str(self.service_type)

class LocationEntity(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    logo = models.URLField(max_length=2500, null=True, blank=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
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
    
    def __str__(self):
        return str(self.name)

class Department(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Doctor(User):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        proxy = False

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
    service_type = models.ForeignKey(ServiceEntity, on_delete= models.CASCADE, default = 1)

    def __str__(self):
        return str(self.name)


class Test(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=150)
    authorised_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.name)

class Sign(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=150)

    def __str__(self):
        return str(self.name)

class Patient(models.Model):
    name = models.CharField(max_length=500)
    contact = models.CharField(max_length=10, unique=True)
    srf_id = models.CharField(max_length=13, unique=True )
    bu_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(default=timezone.now())
    gender = models.CharField(max_length=6, choices=(
        ("MALE","MALE"), ("FEMALE", "FEMALE"), ("OTHERS","OTHERS")
    ))
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
    deceased =models.BooleanField(default=False)
   
    def age(self):
        return str((datetime.date.today() - self.date_of_birth).days // 365) +" years"

    def __str__(self):
        return str(self.name) + " | " + str(self.age()) + " | " + str(self.gender) + " | " + str(self.adhaar_number)

    

class Observation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    observation_for = models.ForeignKey(Test, on_delete=models.CASCADE, validators=[validate_department])
    observation_value = models.CharField(max_length=100)
    observation_date = models.DateField(default=timezone.now())
    observing_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return str(self.patient) +"-"+ str(self.observation_for) +"-"+ str(self.observation_date)

    

class Investigation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    investigation_for = models.ManyToManyField(Sign, related_name="Markers")
    investigation_feedback = models.TextField(max_length=1000)
    investigation_date = models.DateField(default=timezone.now())
    investigating_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, validators=[validate_department])
    def __str__(self) -> str:
        return str(self.patient) +"-"+ str(self.investigation_for) +"-"+ str(self.investigation_date)