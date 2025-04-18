from rest_framework import serializers
from dashboard.models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'image']


class CategorySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = TagCategory
        fields = ['id', 'name', 'tags']


class TagCategorySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['name', 'category']

    def get_category(self, obj):
        return obj.category.name


class ExerciseDetailsSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()
    tags = TagCategorySerializer(many=True)

    class Meta:
        model = Exercise
        fields = [
            'id',
            'title',
            'html_content',
            'video_link',
            'language',
            'tags',
            'image'
        ]

    def get_language(self, obj):
        return obj.language.name


class ExerciseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'title', 'image']


class TrainerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='profile.image')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image']


class CurrentUserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='profile.image')
    trainer = TrainerSerializer(source='profile.trainer', allow_null=True)
    active_until = serializers.DateField(source='profile.active_until', allow_null=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'image', 'trainer', 'active_until'
        ]


class GeneralWorkoutListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'title', 'image']


class PersonalWorkoutListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'title', 'image', 'workout_date']


class SimpleWorkoutExerciseSerializer(serializers.ModelSerializer):
    workoutexercise_id = serializers.IntegerField(source='id')
    exercise_id = serializers.IntegerField(source='exercise.id')
    title = serializers.CharField(source='exercise.title')
    image = serializers.ImageField(source='exercise.image')

    class Meta:
        model = WorkoutExercise
        fields = ['workoutexercise_id', 'exercise_id', 'title', 'image']


class SimpleWorkoutDetailSerializer(serializers.ModelSerializer):
    exercises = SimpleWorkoutExerciseSerializer(source='workout_exercises', many=True)

    class Meta:
        model = Workout
        fields = ['id', 'title', 'workout_date', 'image', 'exercises']


class WorkoutExerciseDetailSerializer(serializers.ModelSerializer):
    exercise = ExerciseDetailsSerializer()

    class Meta:
        model = WorkoutExercise
        fields = [
            'id',
            'exercise',
            'tempo',
            'rest_min',
            'rest_sec',
            'warmup_series',
            'main_series',
            'main_series_reps',
            'warmup',
            'main',
            'comment',
        ]


class WorkoutDetailSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseDetailSerializer(source='workout_exercises', many=True)

    class Meta:
        model = Workout
        fields = ['id', 'title', 'image', 'workout_date', 'exercises']


class UserProfileSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer(source='trainer', allow_null=True)

    class Meta:
        model = UserData
        fields = ['image', 'is_trainer', 'trainer', 'is_active', 'is_hidden', 'active_until']


class FeedbackCreateSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(required=False, allow_blank=True)
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Feedback
        fields = ['comment', 'rating']