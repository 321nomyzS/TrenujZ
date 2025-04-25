function submitForm(event) {
    event.preventDefault();
    const form = document.getElementById('data-form');
    let errors = [];

    const title = document.getElementById('title');
    const videoLink = document.getElementById('video_link');
    const language = document.getElementById('language');
    const imageInput = document.getElementById('image');

    const editorData = CKEDITOR.instances['html_content'].getData();
    const plainText = editorData.replace(/<[^>]*>?/gm, '').trim();

    const hasExistingImage = document.getElementById('exercise-image') !== null;

    // TITLE
    if (title.value.trim() === '') {
        errors.push('Pole tytuł nie może być puste.');
    } else if (title.value.length > 100) {
        errors.push('Tytuł może mieć maksymalnie 100 znaków.');
    }

    // HTML CONTENT
    if (plainText.length === 0) {
        errors.push('Treść ćwiczenia nie może być pusta.');
    }

    // LANGUAGE
    if (!language.value || language.value === '') {
        errors.push('Musisz wybrać język.');
    }

    // IMAGE
    if (imageInput.files.length > 0) {
        const file = imageInput.files[0];
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            errors.push('Plik obrazka musi być typu: JPG, PNG, GIF lub WEBP.');
        }
    } else if (!hasExistingImage) {
        errors.push('Musisz załączyć obrazek.');
    }

    // SHOW ERRORS
    if (errors.length > 0) {
        Swal.fire({
            icon: 'error',
            title: 'Błąd walidacji',
            html: errors.map(e => `<div>${e}</div>`).join(''),
        });
    } else {
        CKEDITOR.instances['html_content'].updateElement();
        form.submit();
    }
}
