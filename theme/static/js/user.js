function validateUserForm(event) {
    event.preventDefault();

    const form = document.getElementById('user-form');
    const errors = [];

    const firstName = document.getElementById('first_name').value.trim();
    const lastName = document.getElementById('last_name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const activeUntil = document.getElementById('active_until').value;
    const imageInput = document.getElementById('image');

    const urlContainsEdit = window.location.href.includes('edit');

    // FIRST NAME
    if (firstName === '') {
        errors.push("Imię jest wymagane.");
    }

    // LAST NAME
    if (lastName === '') {
        errors.push("Nazwisko jest wymagane.");
    }

    // EMAIL
    if (email === '') {
        errors.push("Adres e-mail jest wymagany.");
    } else {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            errors.push("Adres e-mail jest nieprawidłowy.");
        }
    }

    // PASSWORD (tylko jeśli NIE jesteśmy w trybie edycji)
    if (!urlContainsEdit) {
        if (password === '') {
            errors.push("Hasło jest wymagane.");
        } else if (password.length < 6) {
            errors.push("Hasło musi mieć co najmniej 6 znaków.");
        }
    }

    // ACTIVE UNTIL
    if (activeUntil) {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const untilDate = new Date(activeUntil);
        untilDate.setHours(0, 0, 0, 0);
        if (untilDate < today) {
            errors.push("Data aktywności nie może być przeszła.");
        }
    }

    // IMAGE
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


function generateRandomPassword(length = 12) {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+[]{}';
    let password = '';
    for (let i = 0; i < length; i++) {
      password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return password;
  }

  document.addEventListener('DOMContentLoaded', function () {
    const generateBtn = document.getElementById('generate-password');
    const passwordInput = document.getElementById('password');

    generateBtn.addEventListener('click', function () {
      const newPassword = generateRandomPassword();
      passwordInput.value = newPassword;
    });
  });

document.addEventListener('DOMContentLoaded', function () {
  const statusSelect = document.getElementById('status');
  const activeUntilInput = document.getElementById('active_until');

  function toggleActiveUntil() {
    const selected = statusSelect.value;
    if (selected === 'active_until') {
      activeUntilInput.disabled = false;
    } else {
      activeUntilInput.disabled = true;
      activeUntilInput.value = '';
    }
  }

  statusSelect.addEventListener('change', toggleActiveUntil);

  toggleActiveUntil(); // ustaw od razu przy załadowaniu strony
});