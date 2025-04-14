from django.urls import path
from .views import *

urlpatterns = [
    path('tagcategory', TagCategoryView.as_view(), name='tag-category'),
    path('exercises/<int:id>/', ExerciseDetailView.as_view(), name='exercise-detail'),
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
    path('user/current/', CurrentUserView.as_view(), name='current-user'),
    path('user/current/image/', CurrentUserImageView.as_view(), name='current-user-image'),
    path('workouts/general/', GeneralWorkoutListView.as_view(), name='general-workout-list'),
    path('workouts/personal/', PersonalWorkoutListView.as_view(), name='personal-workout-list'),
    path('workout/<int:id>/', WorkoutSimpleDetailView.as_view(), name='workout-detail-simple'),
    path('workoutexercises/<int:id>/', WorkoutExerciseDetailView.as_view(), name='workout-exercise-detail'),
    path('workoutexercises/<int:id>/feedback/', FeedbackCreateView.as_view(), name='workout-exercise-feedback'),
]
