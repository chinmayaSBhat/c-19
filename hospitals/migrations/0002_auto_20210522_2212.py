# Generated by Django 3.0.8 on 2021-05-22 16:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigation',
            name='investigation_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 22, 16, 42, 50, 563930, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='observation',
            name='observation_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 22, 16, 42, 50, 563930, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2021, 5, 22, 16, 42, 50, 562928, tzinfo=utc)),
        ),
    ]