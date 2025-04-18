from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import *
from django.utils.timezone import now


class TagCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trainer = request.user.profile.trainer
        categories = TagCategory.objects.prefetch_related('tags').filter(tags__created_by=trainer).distinct()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ExerciseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        exercise = get_object_or_404(Exercise, pk=id)
        serializer = ExerciseDetailsSerializer(exercise)
        return Response(serializer.data)


class ExerciseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tag_id = request.query_params.get('tag_id', None)
        trainer = request.user.profile.trainer

        if tag_id:
            exercises = Exercise.objects.filter(
                created_by=trainer,
                tags__id=tag_id
            ).distinct()
        else:
            exercises = Exercise.objects.filter(
                created_by=trainer
            )

        serializer = ExerciseListSerializer(exercises, many=True)
        return Response(serializer.data)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)


class CurrentUserImageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        image_url = request.user.profile.image.url if request.user.profile.image else None
        return Response({"image": image_url})


class CurrentUserImageTrainerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trainer = request.user.profile.trainer

        image_url = trainer.profile.image.url if request.user.profile.image else None
        return Response({"image": image_url})


class GeneralWorkoutListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trainer = request.user.profile.trainer
        workouts = Workout.objects.filter(
            is_personal=False,
            visibility=True,
            created_by=trainer
        )
        serializer = GeneralWorkoutListSerializer(workouts, many=True)
        return Response(serializer.data)


class PersonalWorkoutListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        workouts = Workout.objects.filter(
            is_personal=True,
            client=request.user
        )
        serializer = PersonalWorkoutListSerializer(workouts, many=True)
        return Response(serializer.data)


class PersonalWorkoutTodayView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        workouts = Workout.objects.filter(
            is_personal=True,
            client=request.user,
            workout_date=today
        )
        serializer = PersonalWorkoutListSerializer(workouts, many=True)
        return Response(serializer.data)


class WorkoutDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        workout = get_object_or_404(Workout, id=id)

        if workout.is_personal and workout.client != request.user:
            return Response({'success': False, 'detail': 'Brak dostępu do tego treningu.'}, status=403)

        if not workout.is_personal:
            trainer = request.user.profile.trainer
            if workout.created_by != trainer:
                return Response({'success': False, 'detail': 'Brak dostępu do tego treningu.'}, status=403)

        serializer = WorkoutDetailSerializer(workout)
        return Response(serializer.data)


class WorkoutSimpleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        workout = get_object_or_404(Workout, id=id)

        if workout.is_personal and workout.client != request.user:
            return Response({'success': False, 'detail': 'Brak dostępu do treningu'}, status=403)

        if not workout.is_personal:
            trainer = request.user.profile.trainer
            if workout.created_by != trainer:
                return Response({'success': False, 'detail': 'Brak dostępu do treningu'}, status=403)

        serializer = SimpleWorkoutDetailSerializer(workout)
        return Response(serializer.data)


class WorkoutExerciseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        we = get_object_or_404(WorkoutExercise, id=id)

        if we.workout.is_personal and we.workout.client != request.user:
            return Response({'success': False, 'detail': 'Brak dostępu'}, status=403)

        if not we.workout.is_personal:
            trainer = request.user.profile.trainer
            if we.workout.created_by != trainer:
                return Response({'success': False, 'detail': 'Brak dostępu'}, status=403)

        serializer = WorkoutExerciseDetailSerializer(we)
        return Response(serializer.data)


class FeedbackCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        workout_exercise = get_object_or_404(WorkoutExercise, id=id)

        if workout_exercise.workout.is_personal and workout_exercise.workout.client != request.user:
            return Response({'success': False, 'detail': 'Brak dostępu.'}, status=403)

        serializer = FeedbackCreateSerializer(data=request.data)
        if serializer.is_valid():
            Feedback.objects.create(
                workout_exercise=workout_exercise,
                created_by=request.user,
                comment=serializer.validated_data.get('comment', ''),
                rating=serializer.validated_data.get('rating', None)
            )
            return Response({'success': True}, status=201)

        return Response(serializer.errors, status=400)