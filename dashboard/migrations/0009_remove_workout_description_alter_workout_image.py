# Generated by Django 4.2.8 on 2025-04-10 18:53

import dashboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_workout_visibility'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='description',
        ),
        migrations.AlterField(
            model_name='workout',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=dashboard.models.workout_directory_path),
        ),
    ]
