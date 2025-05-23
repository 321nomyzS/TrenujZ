# Generated by Django 4.2.8 on 2025-03-24 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0006_rename_language_name_exerciselanguage_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_personal', models.BooleanField(default=False)),
                ('workout_date', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='workout/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_workouts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tempo', models.TextField(blank=True, null=True)),
                ('rest_min', models.IntegerField(blank=True, null=True)),
                ('rest_sec', models.IntegerField(blank=True, null=True)),
                ('warmup_series', models.IntegerField(blank=True, null=True)),
                ('main_series', models.IntegerField(blank=True, null=True)),
                ('main_series_reps', models.CharField(blank=True, max_length=100, null=True)),
                ('warmup', models.JSONField(blank=True, null=True)),
                ('main', models.JSONField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('alter_exercise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='alternate_for', to='dashboard.exercise')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.exercise')),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_exercises', to='dashboard.workout')),
            ],
        ),
    ]
