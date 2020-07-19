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
admin.site.site_header = "Ahalya"

admin.site.site_title = "Ahalya"

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
            self.exclude+=["admitted_to", "discharged", "discharge_timestamp"] #here!
        return super(PatientAdmin, self).get_form(request, obj, **kwargs)

    actions = ["discharge"]
    search_fields = ("name", "adhaar_number", "contact")

@admin.register(Hospital)
class HospitalAdmin(ImportExportModelAdmin):
    autocomplete_fields = ['admin']
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