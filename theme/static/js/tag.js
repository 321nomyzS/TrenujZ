function submitForm(event) {
    event.preventDefault();

    const form = document.getElementById('tag-form');
    const errors = [];

    const nameInput = document.getElementById('name');
    const categorySelect = document.getElementById('tag-category');
    const imageInput = document.getElementById('image');

    const name = nameInput ? nameInput.value.trim() : '';
    const category = categorySelect ? categorySelect.value : '';

    // NAME
    if (name === '') {
        errors.push("Nazwa tagu jest wymagana.");
    } else if (name.length > 50) {
        errors.push("Nazwa tagu nie może mieć więcej niż 50 znaków.");
    }

    // CATEGORY
    if (category === '') {
        errors.push("Kategoria tagu jest wymagana.");
    }

    // IMAGE (jeśli użytkownik wybrał)
    if (imageInput.files.length > 0) {
        const file = imageInput.files[0];
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            errors.push("Dozwolone formaty obrazka to: JPG, PNG, GIF, WEBP.");
        }
    }

    if (errors.length > 0) {
        Swal.fire({
            icon: 'error',
            title: 'Błąd walidacji',
            html: errors.map(err => `<div>${err}</div>`).join('')
        });
    } else {
        form.submit();
    }
}