# Generated by Django 5.0.8 on 2024-08-29 04:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='img',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='profile_images/'),
            preserve_default=False,
        ),
    ]
