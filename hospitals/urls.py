from django.urls import path
from . import views

app_name = "hospitals"

urlpatterns = [
    path("hospitals/", views.HospitalList.as_view(), name="hospital_list"),
    path("hospitals/<int:pk>", views.HospitalRead.as_view(), name="hospital_read")
]