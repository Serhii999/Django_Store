# Generated by Django 3.1.7 on 2021-03-18 21:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20210316_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='purchase_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='returnpurchase',
            name='time_of_return',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 23, 46, 10, 606468)),
        ),
    ]
