# Generated by Django 3.0.4 on 2020-03-30 15:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200330_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
