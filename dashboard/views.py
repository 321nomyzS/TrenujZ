from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from dashboard.models import *
import shutil


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


def show_tags(request):
    tag_category = TagCategory.objects.all()
    tags = Tag.objects.all()

    return render(request, 'show_tags.html', {"tag_category": tag_category, "tags": tags})


def show_tag(request, id):
    tag = Tag.objects.get(id=id)
    return render(request, 'show_tag.html', {"tag": tag})


def add_tag(request):
    tag_category = TagCategory.objects.all()

    if request.method == 'POST':
        new_tag_category = request.POST['tag-category']
        tag_name = request.POST['name']
        new_tag = Tag(name=tag_name, category_id=new_tag_category)
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


def delete_tag(request, id):
    tag = Tag.objects.get(id=id)

    if tag.image:
        shutil.rmtree(os.path.dirname(os.path.join(settings.MEDIA_ROOT, tag.image.path)))
    tag.delete()

    messages.success(request, "Tag został usunięty pomyślnie")
    return redirect('show_tags')


def add_client(request):
    pass


def edit_client(request, id):
    pass


def show_clients(request):
    pass


def show_client(request, id):
    pass


def delete_client(request, id):
    pass


def login_page(request):
    pass


def logout_tunnel(request):
    pass
