# Generated by Django 5.1.3 on 2024-12-13 07:11

import django.core.validators
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_caritem_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caritem',
            name='date',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, default=True, null=True, validators=[django.core.validators.MinValueValidator(15), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='KG'),
        ),
    ]
