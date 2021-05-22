# Generated by Django 3.0.8 on 2021-05-22 16:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('logo', models.URLField(blank=True, max_length=2500, null=True)),
                ('address1', models.CharField(max_length=200)),
                ('address2', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(max_length=200)),
                ('district', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('pincode', models.CharField(max_length=6)),
                ('phone_area_code', models.CharField(max_length=6)),
                ('contact', models.CharField(max_length=10, unique=True)),
                ('country_code', models.CharField(default='+91', max_length=5)),
                ('active', models.BooleanField(default=True)),
                ('total_isolation_beds', models.SmallIntegerField(default=0)),
                ('total_icu_beds', models.SmallIntegerField(default=0)),
                ('total_ventilated_beds', models.SmallIntegerField(default=0)),
                ('total_high_oxygen_flow_beds', models.SmallIntegerField(default=0)),
                ('total_regular_oxygen_flow_beds', models.SmallIntegerField(default=0)),
                ('admin', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(max_length=100)),
                ('icon_url', models.URLField(blank=True, max_length=2000, null=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('contact', models.CharField(max_length=10, unique=True)),
                ('srf_id', models.CharField(max_length=13, unique=True)),
                ('bu_number', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('date_of_birth', models.DateField(auto_now_add=True)),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHERS', 'OTHERS')], max_length=6)),
                ('country_code', models.CharField(default='+91', max_length=5)),
                ('adhaar_number', models.CharField(blank=True, max_length=12, null=True)),
                ('bed_type', models.CharField(choices=[('ISOLATION', 'ISOLATION'), ('ICU', 'ICU'), ('VENTILATED', 'VENTILATED'), ('HIGH FLOW OXYGEN', 'HIGH FLOW OXYGEN'), ('REGULAR FLOW OXYGEN', 'REGULAR FLOW OXYGEN')], default='ISOLATION', max_length=50)),
                ('admission_timestamp', models.DateTimeField(auto_now=True)),
                ('discharge_timestamp', models.DateTimeField(editable=False, null=True)),
                ('discharged', models.BooleanField(default=False)),
                ('deceased', models.BooleanField(default=False)),
                ('admitted_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitals.Hospital')),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation_value', models.CharField(max_length=100)),
                ('observation_date', models.DateField(default=datetime.datetime(2021, 5, 22, 16, 39, 52, 63915, tzinfo=utc))),
                ('observation_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitals.Test')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitals.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('logo', models.URLField(blank=True, max_length=2500, null=True)),
                ('address1', models.CharField(max_length=200)),
                ('address2', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(max_length=200)),
                ('district', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('pincode', models.CharField(max_length=6)),
                ('phone_area_code', models.CharField(max_length=6)),
                ('contact', models.CharField(max_length=10, unique=True)),
                ('country_code', models.CharField(default='+91', max_length=5)),
                ('active', models.BooleanField(default=True)),
                ('occupied', models.BooleanField(default=False)),
                ('admin', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('associated_hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hospitals.Hospital')),
                ('service_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hospitals.ServiceEntity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Investigation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investigation_feedback', models.TextField(max_length=1000)),
                ('investigation_date', models.DateField(default=datetime.datetime(2021, 5, 22, 16, 39, 52, 64915, tzinfo=utc))),
                ('investigation_for', models.ManyToManyField(related_name='Markers', to='hospitals.Sign')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospitals.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Ambulance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('logo', models.URLField(blank=True, max_length=2500, null=True)),
                ('address1', models.CharField(max_length=200)),
                ('address2', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(max_length=200)),
                ('district', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('pincode', models.CharField(max_length=6)),
                ('phone_area_code', models.CharField(max_length=6)),
                ('contact', models.CharField(max_length=10, unique=True)),
                ('country_code', models.CharField(default='+91', max_length=5)),
                ('active', models.BooleanField(default=True)),
                ('registration_number', models.CharField(max_length=20, unique=True)),
                ('logged_in', models.CharField(choices=[('true', 'true'), ('false', 'false')], default='true', max_length=5)),
                ('occupied', models.CharField(choices=[('true', 'true'), ('false', 'false')], default='false', max_length=5)),
                ('ambulance_type', models.CharField(choices=[('ICU', 'ICU'), ('COLLECTIVE', 'COLLECTIVE'), ('LIFE SUPPORT', 'LIFE SUPPORT'), ('LCV', 'LCV')], max_length=20)),
                ('admin', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('associated_hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hospitals.Hospital')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
