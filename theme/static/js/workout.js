function submitForm(event) {
    event.preventDefault();

    const form = document.querySelector('form');
    let errors = [];

    const title = document.getElementById('title');
    const trainingTypePersonal = document.getElementById('personal-training-radio');
    const trainingTypeGeneral = document.getElementById('general-training-radio');
    const workout_person = document.getElementById('workout-person');
    const workoutDate = document.getElementById('workout_date');
    const visibleYes = document.getElementById('visible-yes-radio');
    const visibleNo = document.getElementById('visible-no-radio');

    // TITLE
    if (!title.value.trim()) {
        errors.push('Pole "Nazwa treningu" nie może być puste.');
    } else if (title.value.length > 100) {
        errors.push('Nazwa treningu może mieć maksymalnie 100 znaków.');
    }

    // TRAINING TYPE (radio)
    const isPersonal = trainingTypePersonal.checked;
    const isGeneral = trainingTypeGeneral.checked;

    if (!isPersonal && !isGeneral) {
        errors.push('Musisz wybrać typ treningu.');
    }

    // STATUS (select)
    if (isPersonal) {
        if (!workout_person || workout_person.value.trim() === '') {
            errors.push('Musisz wybrać osobę dla treningu personalnego.');
        }
    }

    // ACTIVE UNTIL (date)
    if (isPersonal) {
        if (!workoutDate.value || workoutDate.disabled) {
            errors.push('Trening personalny musi mieć ustawioną datę wygaśnięcia.');
        }
    }

    // VISIBILITY (radio)
    if (!visibleYes.checked && !visibleNo.checked) {
        errors.push('Musisz wybrać widoczność treningu.');
    }

    // SHOW ERRORS
    if (errors.length > 0) {
        Swal.fire({
            icon: 'error',
            title: 'Błąd walidacji',
            html: errors.map(e => `<div>${e}</div>`).join(''),
        });
    } else {
        form.submit();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const personalRadio = document.getElementById('personal-training-radio');
    const generalRadio = document.getElementById('general-training-radio');
    const personSelect = document.getElementById('workout-person');
    const dateInput = document.getElementById('workout_date');

    function toggleFields() {
        const isPersonal = personalRadio.checked;

        personSelect.disabled = !isPersonal;
        dateInput.disabled = !isPersonal;

        // Opcjonalnie: resetuj wartość, jeśli nieaktywne
        if (!isPersonal) {
            personSelect.selectedIndex = 0;
            dateInput.value = '';
        }
    }

    // Inicjalizacja na starcie
    toggleFields();

    // Obsługa kliknięć w radio
    personalRadio.addEventListener('change', toggleFields);
    generalRadio.addEventListener('change', toggleFields);
});