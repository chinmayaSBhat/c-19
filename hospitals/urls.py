from django.urls import path
from . import views

app_name = "hospitals"

urlpatterns = [
    path("hospitalList", views.HospitalDetailedList.as_view(), name="hospital_list"),
    path("ambulanceList", views.AmbulanceDetailedList.as_view(), name="ambulance_list"),
    path("medicalServiceList", views.MedicalServiceDetailedList.as_view(), name="medical_service_list")
]