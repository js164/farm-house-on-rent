# Generated by Django 3.1.1 on 2021-07-11 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmuser', '0007_auto_20210711_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmavailble',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
    ]