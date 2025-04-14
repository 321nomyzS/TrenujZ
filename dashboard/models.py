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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class ExerciseLanguage(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


def exercise_directory_path(instance, filename):
    return f'exercise/{instance.id}/{filename}'


class Exercise(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=exercise_directory_path, blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    html_content = models.TextField()

    language = models.ForeignKey(ExerciseLanguage, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='exercises', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

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


def workout_directory_path(instance, filename):
    return f'workout/{instance.id}/{filename}'


class Workout(models.Model):
    title = models.CharField(max_length=100)
    is_personal = models.BooleanField(default=False)
    visibility = models.BooleanField(default=False)

    workout_date = models.DateField(blank=True, null=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='workouts')

    image = models.ImageField(upload_to=workout_directory_path, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_workouts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Personal' if self.is_personal else 'General'} Workout: {self.title}"


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='workout_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    tempo = models.TextField(blank=True, null=True)
    rest_min = models.IntegerField(blank=True, null=True)
    rest_sec = models.IntegerField(blank=True, null=True)

    warmup_series = models.IntegerField(blank=True, null=True)
    main_series = models.IntegerField(blank=True, null=True)
    main_series_reps = models.CharField(blank=True, null=True, max_length=100)

    warmup = models.JSONField(blank=True, null=True)
    main = models.JSONField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    alter_exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True, blank=True, related_name='alternate_for')

    def __str__(self):
        return f"{self.exercise.title} in {self.workout.title}"


class Config(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()

    def __str__(self):
        return f"{self.key} = {self.value}"


class Feedback(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name='feedbacks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"Feedback by {self.created_by.username} on {self.workout_exercise}"