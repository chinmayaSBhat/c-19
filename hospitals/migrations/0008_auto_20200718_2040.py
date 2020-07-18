# Generated by Django 3.0.8 on 2020-07-18 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0007_auto_20200718_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulance',
            name='contact',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='contact',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='medicalservice',
            name='contact',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='contact',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]