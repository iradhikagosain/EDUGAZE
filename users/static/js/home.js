// Hamburger toggle
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('open');
});

// Smooth scroll
document.querySelectorAll('.nav-links a, .hero-buttons a, .cta-buttons a').forEach(link => {
    link.addEventListener('click', e => {
        if(link.getAttribute('href').startsWith('#')) {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if(targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
            
            if(navLinks.classList.contains('open')) {
                hamburger.classList.remove('active');
                navLinks.classList.remove('open');
            }
        }
    });
});

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if(!hamburger.contains(e.target) && !navLinks.contains(e.target) && navLinks.classList.contains('open')) {
        hamburger.classList.remove('active');
        navLinks.classList.remove('open');
    }
});

// Swiper for Courses
const coursesSwiper = new Swiper('.courses-swiper', {
    slidesPerView: 1,
    spaceBetween: 20,
    loop: true,
    navigation: { 
        nextEl: '.swiper-button-next', 
        prevEl: '.swiper-button-prev' 
    },
    breakpoints: { 
        640: { slidesPerView: 1 },
        768: { slidesPerView: 2 }, 
        1024: { slidesPerView: 3 } 
    }
});

// Swiper for Testimonials
const testimonialsSwiper = new Swiper('.testimonials-swiper', {
    slidesPerView: 1,
    spaceBetween: 20,
    loop: true,
    autoplay: { 
        delay: 4000,
        disableOnInteraction: false
    },
    pagination: { 
        el: '.swiper-pagination', 
        clickable: true 
    },
    breakpoints: {
        640: { slidesPerView: 1 },
        768: { slidesPerView: 2 }, 
        1024: { slidesPerView: 3 }
    }
});

// GSAP Animations
if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    // Fade-in sections
    gsap.utils.toArray('.section-title, .card, .course-card, .testimonial-card').forEach(elem => {
        gsap.from(elem, {
            opacity: 0, 
            y: 50, 
            duration: 1, 
            scrollTrigger: {
                trigger: elem, 
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            }
        });
    });

    // Hero stats animation
    const counters = document.querySelectorAll('.stat .count');
    if (counters.length > 0) {
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target') || 
                          (counter.textContent.includes('K') ? 50 : 
                           counter.textContent.includes('%') ? 95 : 500);
            
            gsap.to(counter, {
                textContent: target,
                duration: 2,
                snap: { textContent: 1 },
                scrollTrigger: {
                    trigger: '.hero-stats',
                    start: 'top 80%',
                    toggleActions: 'play none none reverse'
                }
            });
        });
    }

    // Hero text animation
    gsap.from('.hero-text h1', {
        opacity: 0,
        y: 50,
        duration: 1,
        delay: 0.2
    });
    
    gsap.from('.hero-text p', {
        opacity: 0,
        y: 30,
        duration: 1,
        delay: 0.5
    });
    
    gsap.from('.hero-buttons', {
        opacity: 0,
        y: 30,
        duration: 1,
        delay: 0.8
    });
}

// Add data-target attributes to counters
document.addEventListener('DOMContentLoaded', () => {
    const stats = document.querySelectorAll('.stat .count');
    stats[0].setAttribute('data-target', '50');
    stats[1].setAttribute('data-target', '500');
    stats[2].setAttribute('data-target', '95');
});

// Navbar background change on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(93, 18, 24, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
    } else {
        navbar.style.background = '#5D1218';
        navbar.style.backdropFilter = 'none';
    }
});