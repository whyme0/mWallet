# Generated by Django 3.0.4 on 2020-03-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200328_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.DateField(blank=True, verbose_name='Your birth date'),
        ),
    ]
