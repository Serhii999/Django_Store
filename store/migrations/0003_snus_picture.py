# Generated by Django 3.1.7 on 2021-03-13 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_snus'),
    ]

    operations = [
        migrations.AddField(
            model_name='snus',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='snus'),
        ),
    ]
