import re
from urllib.parse import urlparse


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