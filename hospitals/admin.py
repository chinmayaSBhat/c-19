from django.contrib import admin, messages
from .models import *
from django.contrib.auth.models import  Group, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from import_export.admin import ImportExportModelAdmin
from import_export import resources
import datetime

admin.site.unregister(User)
admin.site.unregister(Group)

# Register your models here.
admin.site.site_header = "Arundhathi"

admin.site.site_title = "Arundhathi"

admin.site.index_title = "Hospital Administration"

@admin.register(Patient)
class PatientAdmin(ImportExportModelAdmin):

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser: 
            obj.admitted_to = Hospital.objects.filter(admin=request.user)[0]
        super().save_model(request, obj, form, change)
        

    def get_queryset(self, request):
        qs = super(PatientAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(admitted_to = Hospital.objects.filter(admin=request.user)[0])

    def discharge(self, request, queryset):

        queryset.update(discharged = True, discharge_timestamp=datetime.datetime.now())
        self.message_user(request, "Patients Discharged !")

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            print("Uhoh")
            self.exclude+=["admitted_to", "discharged", "discharge_timestamp", "deceased"] #here!
        return super(PatientAdmin, self).get_form(request, obj, **kwargs)

    actions = ["discharge"]
    search_fields = ("name", "gender" ,"contact", "adhaar_number")
    list_display = ["name","gender", "age", "adhaar_number", "contact"]

    def age(self, obj):
        return str((datetime.date.today() - obj.date_of_birth).days // 365) + " years"

@admin.register(Hospital)
class HospitalAdmin(ImportExportModelAdmin):
    autocomplete_fields = ['admin']
    pass

@admin.register(Doctor)
class DoctorAdmin(ImportExportModelAdmin):
    pass

@admin.register(Ambulance)
class AmbulanceAdmin(ImportExportModelAdmin):
    autocomplete_fields = ['admin']
    pass

@admin.register(MedicalService)
class MedicalServiceAdmin(ImportExportModelAdmin):
    autocomplete_fields = ['admin']
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser: 
            obj.admitted_to = MedicalService.objects.filter(admin=request.user)[0]
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super(MedicalServiceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(admin = request.user)

    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.fields=["occupied"]
        return super(MedicalServiceAdmin, self).get_form(request, obj, **kwargs)



class UserPasswordResource(resources.ModelResource):
    
    def before_import_row(self, row, **kwargs):
        value = row['password']
        row['password'] = make_password(value)
    
    class Meta:
        model = User


@admin.register(User)
class UserAlteredAdmin(UserAdmin, ImportExportModelAdmin):
    search_fields = ("username",)
    resource_class = UserPasswordResource
    

@admin.register(ServiceEntity)
class ServiceEntityAdmin(ImportExportModelAdmin):
    pass
    

@admin.register(Test)
class TestEntityAdmin(ImportExportModelAdmin):
    search_fields = ["name"]

@admin.register(Sign)
class SignsEntityAdmin(ImportExportModelAdmin):
    search_fields = ["name"]

@admin.register(Observation)
class ObservationEntityAdmin(ImportExportModelAdmin):
    
    list_filter = ["observation_date", "patient__gender" ,"observation_for"]
    list_display = ["patient", "observation_for","observation_value"]
    list_editable = ["observation_value"]
    autocomplete_fields = ["patient", "observation_for"]
    search_fields = ["patient__name","patient__adhaar_number"]

    def get_queryset(self, request):
        qs = super(ObservationEntityAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif isinstance(request.user, Doctor):
            qs.filter(patient__admitted_to = Hospital.objects.filter(admin=request.user)[0], observing_doctor= request.user)
        else:
            return qs.filter(patient__admitted_to = Hospital.objects.filter(admin=request.user)[0])
    
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if isinstance(request.user, Doctor):
            print("Doctor is observing :)")
            self.exclude+=["observing_doctor"] #here!
        return super(ObservationEntityAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if isinstance(request.user, Doctor): 
            obj.observing_doctor = request.user
        super().save_model(request, obj, form, change)

@admin.register(Investigation)
class InvestigationEntityAdmin(ImportExportModelAdmin):

    list_filter = ["investigation_date", "patient__gender" ,"investigation_for"]
    list_display = ["patient", "investigation_for_signs","investigation_feedback"]
    list_editable = ["investigation_feedback"]
    autocomplete_fields = ["patient", "investigation_for"]
    search_fields = ["patient__name","patient__adhaar_number"]

    def get_queryset(self, request):
        qs = super(InvestigationEntityAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif isinstance(request.user, Doctor):
            qs.filter(patient__admitted_to = Hospital.objects.filter(admin=request.user)[0], investigating_doctor= request.user)
        else:
            return qs.filter(patient__admitted_to = Hospital.objects.filter(admin=request.user)[0])

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if isinstance(request.user, Doctor):
            print("Doctor is investigating :)")
            self.exclude+=["investigating_doctor"] #here!
        return super(InvestigationEntityAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if isinstance(request.user, Doctor): 
            obj.investigating_doctor = request.user
        super().save_model(request, obj, form, change)


    def investigation_for_signs(self, obj):
        investigation_for_string = ""
        for x in obj.investigation_for.all():

            investigation_for_string = investigation_for_string+ x.name+ ", " 
        print(investigation_for_string)
        return investigation_for_string
    
