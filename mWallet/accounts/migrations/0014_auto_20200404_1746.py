# Generated by Django 3.0.4 on 2020-04-04 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20200403_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Your birth date'),
        ),
    ]
