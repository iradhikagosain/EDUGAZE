document.addEventListener('DOMContentLoaded', function() {
    const mobileToggle = document.getElementById('mobileMenuToggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');

    // Mobile menu toggle
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-open');
            mainContent.classList.toggle('mobile-open');
            this.querySelector('i').className = sidebar.classList.contains('mobile-open') ? 'fas fa-times' : 'fas fa-bars';
        });
    }

    // Sidebar nav scroll
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            if(this.getAttribute('href').startsWith('#')){
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if(target){
                    window.scrollTo({ top: target.offsetTop - 80, behavior:'smooth' });
                }
            }
        });
    });
});
