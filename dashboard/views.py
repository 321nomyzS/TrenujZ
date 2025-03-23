from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from dashboard.models import *
from datetime import datetime

import shutil
import hashlib
import os

def home(request):
    return render(request, 'base.html')


def add_exercise(request):
    pass


def show_exercises(request):
    pass


def show_exercise(request, id):
    pass


def edit_exercise(request, id):
    pass


def delete_exercise(request, id):
    pass


def add_training(request):
    pass


def duplicate_training(request, id):
    pass


def show_training(request):
    pass


def show_general_training(request, id):
    pass


def show_personal_training(request, id):
    pass


def edit_general_training(request, id):
    pass


def edit_personal_training(request, id):
    pass


def delete_general_training(request, id):
    pass


def delete_personal_training(request, id):
    pass


@login_required
def show_tags(request):
    tag_category = TagCategory.objects.all()
    tags = Tag.objects.all()

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

        if active_until_raw != "":
            profile.active_until = datetime.strptime(active_until_raw, "%Y-%m-%d").date()

        if request.FILES:
            image = request.FILES['photo']

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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        status = request.POST.get('status')
        active_until_raw = request.POST.get('active_until')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
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

        if active_until_raw != "":
            profile.active_until = datetime.strptime(active_until_raw, "%Y-%m-%d").date()

        if request.FILES:
            image = request.FILES['photo']

            if image:
                md5 = hashlib.md5()
                for chunk in image.chunks():
                    md5.update(chunk)
                file_hash = md5.hexdigest()

                extension = os.path.splitext(image.name)[1]
                new_name = f"{file_hash}{extension}"
                image.name = new_name
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

    profile.is_hidden = True
    profile.save()

    return redirect('show_users')


@csrf_protect
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if not user.is_staff and not user.is_superuser:
            messages.error(request, "Nie masz uprawnień")
            return render(request, 'login.html')
        if user:
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
