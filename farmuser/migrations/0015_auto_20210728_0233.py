# Generated by Django 3.1.1 on 2021-07-27 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmuser', '0014_auto_20210728_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmbooking',
            name='No_of_People',
            field=models.IntegerField(default=1),
        ),
    ]
