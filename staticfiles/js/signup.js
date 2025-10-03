function showTeacherForm() {
    document.querySelector('.role-selection').style.display = 'none';
    document.getElementById('teacher-form').style.display = 'block';
    document.getElementById('student-form').style.display = 'none';
}

function showStudentForm() {
    document.querySelector('.role-selection').style.display = 'none';
    document.getElementById('student-form').style.display = 'block';
    document.getElementById('teacher-form').style.display = 'none';
}

function showRoleSelection() {
    document.querySelector('.role-selection').style.display = 'flex';
    document.getElementById('teacher-form').style.display = 'none';
    document.getElementById('student-form').style.display = 'none';
}

// Ensure forms are hidden on page load
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('teacher-form').style.display = 'none';
    document.getElementById('student-form').style.display = 'none';
    
    // Add click handlers for role cards
    document.querySelector('.teacher-role').addEventListener('click', showTeacherForm);
    document.querySelector('.student-role').addEventListener('click', showStudentForm);
});

// File upload display
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const label = this.nextElementSibling;
            if (this.files.length > 0) {
                label.innerHTML = `<span class="upload-icon">✓</span> ${this.files[0].name}`;
            } else {
                label.innerHTML = `<span class="upload-icon">📁</span> Choose File`;
            }
        });
    });
});