from django.urls import path
from . import views
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

app_name = "hospitals"

urlpatterns = [
    path('token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("hospitalList", views.HospitalList.as_view(), name="hospital_list"),
    path("ambulanceList", views.AmbulanceList.as_view(), name="ambulance_list"),
    path("ambulanceDetail", views.AmbulanceDetail.as_view(), name="ambulance_detail"),
    path("ambulanceUpdate",views.AmbulanceUpdate.as_view(), name="ambulance_update"),
    path("medicalServiceList", views.MedicalServiceList.as_view(), name="medical_service_list")
]