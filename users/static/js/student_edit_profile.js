
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.edit-profile-form');

    if(form) {
        form.addEventListener('submit', (e) => {
            const requiredFields = form.querySelectorAll('input[required], select[required]');
            let valid = true;

            requiredFields.forEach(field => {
                if(!field.value.trim()) {
                    valid = false;
                    field.style.borderColor = '#e74c3c';
                } else {
                    field.style.borderColor = '';
                }
            });

            if(!valid) {
                e.preventDefault();
                alert('Please fill all required fields!');
            }
        });
    }
});
