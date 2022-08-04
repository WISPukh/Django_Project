# Generated by Django 4.0.5 on 2022-08-04 07:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator('\\d{11}', 'Enter a valid phone number', code='phone number')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='region',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
