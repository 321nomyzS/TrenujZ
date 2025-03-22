import hashlib
import os
from datetime import date
from django.db import models


def exercise_tag_directory_path(instance, filename):
    return f'tags/{instance.id}/{filename}'


class TagCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(TagCategory, on_delete=models.CASCADE, related_name='tags')
    image = models.ImageField(upload_to=exercise_tag_directory_path, blank=True, null=True)

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class ExerciseLanguage(models.Model):
    language_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.language_name


def exercise_directory_path(instance, filename):
    return f'exercise/{instance.id}/{filename}'


class Exercise(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    image = models.ImageField(upload_to=exercise_directory_path, blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    html_content = models.TextField()

    language = models.ForeignKey(ExerciseLanguage, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='exercises', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

