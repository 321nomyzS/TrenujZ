from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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


def person_directory_path(instance, filename):
    return f'user/{instance.id}/{filename}'


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to=person_directory_path, default='default/user.jpg')

    is_trainer = models.BooleanField(default=False)
    trainer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="trainees")

    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)
    active_until = models.DateField(blank=True, null=True)

    def is_account_active(self):
        if self.is_hidden:
            return False
        if self.active_until and self.active_until < timezone.now().date():
            return False
        return self.is_active
