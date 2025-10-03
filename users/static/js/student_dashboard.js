
document.addEventListener("DOMContentLoaded", function () {
    const mobileMenuToggle = document.getElementById("mobileMenuToggle");
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("mainContent");

    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener("click", () => {
            sidebar.classList.toggle("mobile-open");
        });
    }

    document.addEventListener("click", function (e) {
        if (
            sidebar.classList.contains("mobile-open") &&
            !sidebar.contains(e.target) &&
            !mobileMenuToggle.contains(e.target)
        ) {
            sidebar.classList.remove("mobile-open");
        }
    });
});
