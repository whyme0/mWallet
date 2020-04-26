# Generated by Django 3.0.4 on 2020-04-23 17:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.CharField(help_text="Don't change token manually. It's exist to reset user password", max_length=20, validators=[django.core.validators.MinLengthValidator(20)]),
        ),
    ]