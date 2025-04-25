from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.utils.dateparse import parse_date
from dashboard.models import *
import dashboard.validation as validation
from datetime import datetime

import shutil
import hashlib
import os


def home(request):
    return render(request, 'base.html')


@login_required
def add_exercise(request):
    tags = Tag.objects.filter(created_by=request.user)
    tags_category = TagCategory.objects.all()
    languages = ExerciseLanguage.objects.all()

    if request.method == 'POST':
        errors = validation.validate_exercise_data(request)
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'add_exercise.html', {
                'languages': ExerciseLanguage.objects.all(),
                'tags': Tag.objects.all()
            })

        title = request.POST.get('title')
        language_name = request.POST.get('language')
        video_link = request.POST.get('video_link')
        html_content = request.POST.get('html_content')
        selected_tag_ids = request.POST.getlist('tags')

        exercise = Exercise(
            title=title,
            video_link=video_link,
            html_content=html_content,
            created_by=request.user
        )

        language = ExerciseLanguage.objects.get(name=language_name)
        exercise.language = language
        exercise.save()

        if selected_tag_ids:
            selected_tags = Tag.objects.filter(id__in=selected_tag_ids, created_by=request.user)
            exercise.tags.set(selected_tags)

        if request.FILES:
            image = request.FILES['image']

            if image:
                md5 = hashlib.md5()
                for chunk in image.chunks():
                    md5.update(chunk)
                file_hash = md5.hexdigest()

                extension = os.path.splitext(image.name)[1]
                new_name = f"{file_hash}{extension}"
                image.name = new_name

                exercise.image = image
        exercise.save()

        messages.success(request, "Ćwiczenie zostało dodane pomyślnie")
        return redirect('show_exercises')

    return render(request, 'add_exercise.html', {"tags": tags, "tags_category": tags_category, "languages": languages})


@login_required
def show_exercises(request):
    exercises = Exercise.objects.filter(created_by=request.user)

    return render(request, "show_exercises.html", {"exercises": exercises})


@login_required
def show_exercise(request, id):
    exercise = Exercise.objects.get(id=id)
    tags_category = TagCategory.objects.all()
    tags = Tag.objects.filter(created_by=request.user)

    return render(request, "show_exercise.html", {"exercise": exercise, "tags_category": tags_category, "tags": tags})


@login_required
def edit_exercise(request, id):
    exercise = Exercise.objects.get(id=id)
    tags = Tag.objects.filter(created_by=request.user)
    tags_category = TagCategory.objects.all()
    languages = ExerciseLanguage.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        language_name = request.POST.get('language')
        video_link = request.POST.get('video_link')
        html_content = request.POST.get('html_content')
        selected_tag_ids = request.POST.getlist('tags')

        exercise.title = title
        exercise.video_link = video_link
        exercise.html_content = html_content

        language = ExerciseLanguage.objects.get(name=language_name)
        exercise.language = language
        exercise.save()

        selected_tags = Tag.objects.filter(id__in=selected_tag_ids, created_by=request.user)
        exercise.tags.set(selected_tags)

        if request.FILES:
            image = request.FILES['image']

            if image:
                md5 = hashlib.md5()
                for chunk in image.chunks():
                    md5.update(chunk)
                file_hash = md5.hexdigest()

                extension = os.path.splitext(image.name)[1]
                new_name = f"{file_hash}{extension}"
                image.name = new_name
                exercise.image.delete()

                exercise.image = image
        exercise.save()

        messages.success(request, "Ćwiczenie zostało zaktualizowane pomyślnie")
        return redirect('show_exercises')

    return render(request, 'edit_exercise.html', {"exercise": exercise, "tags": tags, "tags_category": tags_category, "languages": languages})


@login_required
def delete_exercise(request, id):
    exercise = Exercise.objects.get(id=id)

    if exercise.image:
        shutil.rmtree(os.path.dirname(os.path.join(settings.MEDIA_ROOT, exercise.image.path)))
    exercise.delete()

    messages.success(request, "Ćwiczenie zostało usunięte pomyślnie")
    return redirect('show_exercises')


def _parse_json_reps(request, row_index, rep_type, max_series=4):
    """
    Zbiera powtórzenia z formularza i zwraca listę wartości jako JSON, np. [12, 10, 8]
    """
    reps = []
    for i in range(1, max_series + 1):
        key = f"{rep_type}-series-{i}-rep-{row_index}"
        val = request.POST.get(key)
        if val:
            reps.append(val)
    return reps


def add_training(request):
    exercises = Exercise.objects.filter(created_by=request.user)
    clients = User.objects.filter(profile__trainer=request.user)

    if request.method == 'POST':
        post = request.POST
        title = post.get('title', '')
        is_personal = post.get('training-type') == 'personal'
        visibility = post.get('visible-radio') == 'yes'
        workout_date = parse_date(post.get('workout_date')) if is_personal else None

        client_id = post.get('workout-person', None)
        client = User.objects.get(id=client_id) if client_id is not None else None

        workout = Workout.objects.create(
            title=title,
            is_personal=is_personal,
            workout_date=workout_date,
            client=client,
            created_by=request.user,
            visibility=visibility
        )

        if request.FILES:
            image = request.FILES['image']

            if image:
                md5 = hashlib.md5()
                for chunk in image.chunks():
                    md5.update(chunk)
                file_hash = md5.hexdigest()

                extension = os.path.splitext(image.name)[1]
                new_name = f"{file_hash}{extension}"
                image.name = new_name
                workout.image.delete()

                workout.image = image
        else:
            workout.image = Config.objects.get(key="default_workout_image").value
        workout.save()

        try:
            row_count = int(post.get('rowCount', '0'))
        except ValueError:
            row_count = 0

        for i in range(1, row_count + 1):
            exercise_id = post.get(f'exercise-id-{i}')
            if not exercise_id:
                continue

            try:
                exercise = Exercise.objects.get(pk=exercise_id)
            except Exercise.DoesNotExist:
                continue

            tempo = post.get(f'tempo-{i}')
            rest_min = post.get(f'rest-min-{i}')
            rest_sec = post.get(f'rest-sec-{i}')
            warmup_series = post.get(f'warmup-series-{i}')
            main_series = post.get(f'main-series-{i}')
            main_series_reps = post.get(f'main-series-reps-{i}')
            comment = post.get(f'comment-{i}')
            alter_exercise_id = post.get(f'alter-exercise-id-{i}')

            warmup_json = _parse_json_reps(request, i, 'warmup')
            main_json = _parse_json_reps(request, i, 'main')

            alter_exercise = None
            if alter_exercise_id:
                try:
                    alter_exercise = Exercise.objects.get(pk=alter_exercise_id)
                except Exercise.DoesNotExist:
                    pass

            WorkoutExercise.objects.create(
                workout=workout,
                exercise=exercise,
                tempo=tempo,
                rest_min=int(rest_min) if rest_min else None,
                rest_sec=int(rest_sec) if rest_sec else None,
                warmup_series=int(warmup_series) if warmup_series else None,
                main_series=int(main_series) if main_series else None,
                main_series_reps=main_series_reps,
                warmup=warmup_json,
                main=main_json,
                comment=comment,
                alter_exercise=alter_exercise
            )
        messages.success(request, "Trening został dodany pomyślnie")
        return redirect('show_trainings')

    return render(request, 'add_training.html', {
        "exercises": exercises,
        "clients": clients
    })


def duplicate_training(request, id):
    original_workout = Workout.objects.get(id=id)

    duplicated_workout = Workout.objects.create(
        title=original_workout.title,
        is_personal=original_workout.is_personal,
        workout_date=original_workout.workout_date,
        client=original_workout.client,
        created_by=original_workout.created_by,
        visibility=False
    )

    original_exercises = WorkoutExercise.objects.filter(workout=original_workout)
    for original in original_exercises:
        WorkoutExercise.objects.create(
            workout=duplicated_workout,
            exercise=original.exercise,
            tempo=original.tempo,
            rest_min=original.rest_min,
            rest_sec=original.rest_sec,
            warmup_series=original.warmup_series,
            main_series=original.main_series,
            main_series_reps=original.main_series_reps,
            warmup=original.warmup,
            main=original.main,
            comment=original.comment,
            alter_exercise=original.alter_exercise
        )

    if original_workout.image and original_workout.image.name != Config.objects.get(key="default_workout_image").value:
        original_path = original_workout.image.path
        file_name = os.path.basename(original_path)

        new_folder = os.path.join(settings.MEDIA_ROOT, 'workout', str(duplicated_workout.id))
        os.makedirs(new_folder, exist_ok=True)

        new_file_path = os.path.join(new_folder, file_name)
        shutil.copyfile(original_path, new_file_path)

        relative_path = os.path.join('workout', str(duplicated_workout.id), file_name)
        duplicated_workout.image = relative_path
        duplicated_workout.save()
    elif not original_workout.image:
        duplicated_workout.image = Config.objects.get(key="default_workout_image").value
        duplicated_workout.save()

    messages.success(request, "Trening został zduplikowany")
    return redirect('edit_training', id=duplicated_workout.id)


def show_trainings(request):
    workouts = Workout.objects.filter(created_by=request.user)

    return render(request, 'show_trainings.html', {'workouts': workouts})


def show_training(request, id):
    workout = Workout.objects.get(id=id)
    workout_exercises = WorkoutExercise.objects.filter(workout=workout)
    feedback = Feedback.objects.filter(workout_exercise__workout=workout)

    return render(request, 'show_training.html', {'feedback': feedback,'training': workout, 'workout_exercises': workout_exercises})


def edit_training(request, id):
    workout = Workout.objects.get(id=id)
    exercises = Exercise.objects.filter(created_by=request.user)
    clients = User.objects.filter(profile__trainer=request.user)
    workout_exercises = WorkoutExercise.objects.filter(workout=workout)

    if request.method == 'POST':
        post = request.POST
        workout.title = post.get('title', '')
        workout.visibility = post.get('visible-radio') == 'yes'

        if workout.is_personal:
            workout.workout_date = parse_date(post.get('workout_date')) if workout.is_personal else None

        client_id = post.get('workout-person', None)
        workout.client = User.objects.get(id=client_id) if client_id else None

        # Obsługa obrazu
        if request.FILES:
            image = request.FILES['image']
            if image:
                md5 = hashlib.md5()
                for chunk in image.chunks():
                    md5.update(chunk)
                file_hash = md5.hexdigest()
                extension = os.path.splitext(image.name)[1]
                new_name = f"{file_hash}{extension}"
                image.name = new_name

                if workout.image.path != Config.objects.get(key="default_workout_image").value:
                    workout.image.delete()
                workout.image = image

        workout.save()

        # Usuń stare ćwiczenia
        WorkoutExercise.objects.filter(workout=workout).delete()

        try:
            row_count = int(post.get('rowCount', '0'))
        except ValueError:
            row_count = 0

        for i in range(1, row_count + 1):
            exercise_id = post.get(f'exercise-id-{i}')
            if not exercise_id:
                continue

            try:
                exercise = Exercise.objects.get(pk=exercise_id)
            except Exercise.DoesNotExist:
                continue

            tempo = post.get(f'tempo-{i}')
            rest_min = post.get(f'rest-min-{i}')
            rest_sec = post.get(f'rest-sec-{i}')
            warmup_series = post.get(f'warmup-series-{i}')
            main_series = post.get(f'main-series-{i}')
            main_series_reps = post.get(f'main-series-reps-{i}')
            comment = post.get(f'comment-{i}')
            alter_exercise_id = post.get(f'alter-exercise-id-{i}')

            warmup_json = _parse_json_reps(request, i, 'warmup')
            main_json = _parse_json_reps(request, i, 'main')

            alter_exercise = None
            if alter_exercise_id:
                try:
                    alter_exercise = Exercise.objects.get(pk=alter_exercise_id)
                except Exercise.DoesNotExist:
                    pass

            WorkoutExercise.objects.create(
                workout=workout,
                exercise=exercise,
                tempo=tempo,
                rest_min=int(rest_min) if rest_min else None,
                rest_sec=int(rest_sec) if rest_sec else None,
                warmup_series=int(warmup_series) if warmup_series else None,
                main_series=int(main_series) if main_series else None,
                main_series_reps=main_series_reps,
                warmup=warmup_json,
                main=main_json,
                comment=comment,
                alter_exercise=alter_exercise
            )

        messages.success(request, "Trening został zaktualizowany")
        return redirect('show_trainings')

    return render(request, 'edit_training.html', {
        "training": workout,
        "workout_exercises": workout_exercises,
        "exercises": exercises,
        "clients": clients
    })


@login_required
@csrf_protect
def delete_training(request, id):
    workout = Workout.objects.get(id=id)
    workout_exercises = WorkoutExercise.objects.filter(workout=workout)

    if workout.image:
        if workout.image.path != Config.objects.get(key="default_workout_image").value:
            if os.path.exists(os.path.dirname(os.path.join(settings.MEDIA_ROOT, workout.image.path))):
                shutil.rmtree(os.path.dirname(os.path.join(settings.MEDIA_ROOT, workout.image.path)))

    for workout_exercise in workout_exercises:
        workout_exercise.delete()

    workout.delete()
    messages.success(request, "Trening został pomyślnie usunięty")

    return redirect('show_trainings')


@login_required
def show_tags(request):
    tag_category = TagCategory.objects.all()
    tags = Tag.objects.all().order_by('category')

    return render(request, 'show_tags.html', {"tag_category": tag_category, "tags": tags})


@login_required
def show_tag(request, id):
    tag = Tag.objects.get(id=id)
    return render(request, 'show_tag.html', {"tag": tag})


@login_required
def add_tag(request):
    tag_category = TagCategory.objects.all()

    if request.method == 'POST':
        new_tag_category = request.POST['tag-category']
        tag_name = request.POST['name']
        new_tag = Tag(name=tag_name, category_id=new_tag_category, created_by=request.user)
        new_tag.save()

        if request.FILES:
            image = request.FILES['image']

            if image:
                md5 = hashlib.md5()
                for chunk in image.chunks():
                    md5.update(chunk)
                file_hash = md5.hexdigest()

                extension = os.path.splitext(image.name)[1]
                new_name = f"{file_hash}{extension}"
                image.name = new_name

                new_tag.image = image
        new_tag.save()

        messages.success(request, "Tag został dodany pomyślnie")
        return redirect('show_tags')

    return render(request, 'add_tag.html', {"tag_category": tag_category})


@login_required
def edit_tag(request, id):
    tag = Tag.objects.get(id=id)
    tag_category = TagCategory.objects.all()

    if request.method == 'POST':
        new_tag_category = request.POST['tag-category']
        tag_name = request.POST['name']
        tag.name = tag_name
        tag.category_id = new_tag_category

        if request.FILES:
            image = request.FILES['image']

            if image:
                md5 = hashlib.md5()
                for chunk in image.chunks():
                    md5.update(chunk)
                file_hash = md5.hexdigest()

                extension = os.path.splitext(image.name)[1]
                new_name = f"{file_hash}{extension}"
                image.name = new_name

                tag.image.delete()
                tag.image = image
        tag.save()

        messages.success(request, "Tag został zaktualizowany pomyślnie")
        return redirect('show_tags')

    return render(request, 'edit_tag.html', {"tag": tag, "tag_category": tag_category})


@login_required
def delete_tag(request, id):
    tag = Tag.objects.get(id=id)

    if tag.image:
        shutil.rmtree(os.path.dirname(os.path.join(settings.MEDIA_ROOT, tag.image.path)))
    tag.delete()

    messages.success(request, "Tag został usunięty pomyślnie")
    return redirect('show_tags')


@login_required
def add_user(request):
    if request.method == 'POST':
        errors = validation.validate_user_data(request)
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'add_user.html')

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        status = request.POST.get('status')
        active_until_raw = request.POST.get('active_until')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        profile, _ = UserData.objects.get_or_create(user=user)

        profile.trainer = request.user

        if status == "active":
            profile.is_active = True
        elif status == "inactive":
            profile.is_active = False
        else:
            profile.is_active = True

        if active_until_raw:
            profile.active_until = datetime.strptime(active_until_raw, "%Y-%m-%d").date()
        else:
            profile.active_until = None

        if request.FILES:
            image = request.FILES['image']

            if image:
                md5 = hashlib.md5()
                for chunk in image.chunks():
                    md5.update(chunk)
                file_hash = md5.hexdigest()

                extension = os.path.splitext(image.name)[1]
                new_name = f"{file_hash}{extension}"
                image.name = new_name

                profile.image = image
        profile.save()

        messages.success(request, "Użytkownik został dodany pomyślnie")
        return redirect('show_users')

    return render(request, 'add_user.html')


@login_required
def edit_user(request, id):
    user = User.objects.get(id=id)

    if request.method == 'POST':
        errors = validation.validate_user_data(request, editing_user_id=id)
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'edit_user.html', {"client": user})

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        status = request.POST.get('status')
        active_until_raw = request.POST.get('active_until')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = email

        if password:
            user.set_password(password)

        user.save()

        profile, _ = UserData.objects.get_or_create(user=user)

        if status == "active":
            profile.is_active = True
        elif status == "inactive":
            profile.is_active = False
        else:
            profile.is_active = True

        if active_until_raw:
            profile.active_until = datetime.strptime(active_until_raw, "%Y-%m-%d").date()
        else:
            profile.active_until = None

        if request.FILES:
            image = request.FILES['image']

            if image:
                md5 = hashlib.md5()
                for chunk in image.chunks():
                    md5.update(chunk)
                file_hash = md5.hexdigest()

                extension = os.path.splitext(image.name)[1]
                new_name = f"{file_hash}{extension}"
                image.name = new_name

                if profile.image.url != "/media" + Config.objects.get(key="default_user_image").value:
                    profile.image.delete()
                profile.image = image
        profile.save()

        messages.success(request, "Użytkownik został zaktualizowany pomyślnie")
        return redirect('show_users')
    return render(request, "edit_user.html", {"client": user})


@login_required
def show_users(request):
    users = User.objects.filter(profile__trainer=request.user).filter(profile__is_hidden=0)

    return render(request, 'show_users.html', {"users": users})


@login_required
def show_user(request, id):
    user = User.objects.get(id=id)

    return render(request, "show_user.html", {"client": user})


@login_required
def delete_user(request, id):
    user = User.objects.get(id=id)
    profile = user.profile

    is_related = (
        user.created_workouts.exists() or
        user.workouts.exists() or
        user.trainees.exists() or
        user.tag_set.exists() or
        user.exercise_set.exists() or
        user.feedback_set.exists()
    )

    if is_related:
        profile.is_hidden = True
        profile.save()
        messages.success(request, "Użytkownik został ukryty pomyślnie")
    else:
        user.delete()
        messages.success(request, "Użytkownik został usunięty pomyślnie")

    return redirect('show_users')


@csrf_protect
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            if not user.is_staff and not user.is_superuser:
                messages.error(request, "Nie masz uprawnień")
                return render(request, 'login.html')
            else:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Niepoprawne dane logowania")
            return render(request, 'login.html')
    return render(request, 'login.html')


def logout_tunnel(request):
    logout(request)
    messages.info(request, "Zostałeś wylogowany")
    return redirect('login')


def tmp(requset):
    return render(requset, 'tmp.html')
