document.addEventListener('DOMContentLoaded', function() {
    const confirmCheckbox = document.getElementById('confirm-delete');
    const deleteBtn = document.getElementById('delete-btn');
    
    confirmCheckbox.addEventListener('change', function() {
        deleteBtn.disabled = !this.checked;
    });
    
    // Add confirmation before submitting
    const deleteForm = document.querySelector('.delete-form');
    deleteForm.addEventListener('submit', function(e) {
        if (!confirm('Are you absolutely sure you want to delete your account? This action cannot be undone.')) {
            e.preventDefault();
        }
    });
});