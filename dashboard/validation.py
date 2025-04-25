import re
from urllib.parse import urlparse
from django.contrib.auth import get_user_model


def validate_user_data(request, editing_user_id=None):
    errors = []
    User = get_user_model()

    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()
    status = request.POST.get('status', '').strip()
    image = request.FILES.get('image')

    # FIRST NAME
    if not first_name:
        errors.append("Imię nie może być puste.")
    elif len(first_name) > 50:
        errors.append("Imię może mieć maksymalnie 50 znaków.")

    # LAST NAME
    if not last_name:
        errors.append("Nazwisko nie może być puste.")
    elif len(last_name) > 50:
        errors.append("Nazwisko może mieć maksymalnie 50 znaków.")

    # EMAIL
    if not email:
        errors.append("Email nie może być pusty.")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append("Email musi być poprawnym adresem email.")
    else:
        # Sprawdź unikalność e-maila
        existing_user = User.objects.filter(email=email).exclude(id=editing_user_id).first()
        if existing_user:
            errors.append("Ten adres e-mail jest już używany.")

    # PASSWORD
    if not editing_user_id:
        if not password:
            errors.append("Hasło nie może być puste.")
        elif len(password) < 8:
            errors.append("Hasło musi mieć co najmniej 8 znaków.")

    # STATUS
    if status not in ['active', 'inactive', 'active_until']:
        errors.append("Status musi być 'active' lub 'inactive'.")

    # IMAGE
    if image:
        valid_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if image.content_type not in valid_mime_types:
            errors.append("Plik zdjęcia musi być typu JPG, PNG, GIF lub WEBP.")

    return errors


def validate_exercise_data(request):
    errors = []

    title = request.POST.get('title', '').strip()
    video_link = request.POST.get('video_link', '').strip()
    html_content = request.POST.get('html_content', '').strip()
    language = request.POST.get('language', '').strip()
    image = request.FILES.get('image')

    # TITLE
    if not title:
        errors.append("Pole tytuł nie może być puste.")
    elif len(title) > 100:
        errors.append("Tytuł może mieć maksymalnie 100 znaków.")

    # VIDEO LINK
    if video_link:
        try:
            result = urlparse(video_link)
            if not all([result.scheme, result.netloc]):
                errors.append("Link do wideo musi być poprawnym adresem URL.")
        except Exception:
            errors.append("Link do wideo musi być poprawnym adresem URL.")

    # HTML_CONTENT (sprawdzamy czysty tekst bez HTML)
    plain_text = re.sub(r'<[^>]+>', '', html_content).strip()
    if not plain_text:
        errors.append("Treść ćwiczenia nie może być pusta.")

    # LANGUAGE
    if not language:
        errors.append("Musisz wybrać język.")

    # IMAGE
    if not image:
        errors.append("Musisz załączyć obrazek.")
    else:
        valid_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if image.content_type not in valid_mime_types:
            errors.append("Plik obrazka musi być typu JPG, PNG, GIF lub WEBP.")

    return errors