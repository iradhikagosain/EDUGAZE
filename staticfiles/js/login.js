// Hamburger menu toggle
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('open');
});

// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleButton = document.querySelector('.toggle-password');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleButton.textContent = '👁️‍🗨️';
        toggleButton.setAttribute('aria-label', 'Hide password');
    } else {
        passwordInput.type = 'password';
        toggleButton.textContent = '👁️';
        toggleButton.setAttribute('aria-label', 'Show password');
    }
}

// Fill demo credentials
function fillDemoCredentials(role) {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    
    if (role === 'teacher') {
        emailInput.value = 'teacher@demo.com';
        passwordInput.value = 'demo123';
    } else if (role === 'student') {
        emailInput.value = 'student@demo.com';
        passwordInput.value = 'demo123';
    }
    
    // Add visual feedback
    const demoCard = event.currentTarget;
    demoCard.style.borderColor = '#A02A2D';
    demoCard.style.backgroundColor = '#fff5f5';
    
    setTimeout(() => {
        demoCard.style.borderColor = '#e9ecef';
        demoCard.style.backgroundColor = '#fff';
    }, 2000);
    
    // Show confirmation message
    showMessage(`Demo ${role} credentials filled!`, 'success');
}

// Form submission handling
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleLoginSubmission(this);
        });
    }
    
    // Social login buttons
    const socialButtons = document.querySelectorAll('.btn-social');
    socialButtons.forEach(button => {
        button.addEventListener('click', function() {
            const platform = this.classList[1].replace('btn-', '');
            handleSocialLogin(platform);
        });
    });
    
    // Add keyboard accessibility to demo cards
    const demoCards = document.querySelectorAll('.demo-card');
    demoCards.forEach(card => {
        card.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const role = this.querySelector('.demo-role').textContent.toLowerCase().includes('teacher') ? 'teacher' : 'student';
                fillDemoCredentials(role);
            }
        });
        
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
    });
});

function handleLoginSubmission(form) {
    const submitBtn = form.querySelector('.btn-login');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    const email = form.querySelector('#email').value;
    const password = form.querySelector('#password').value;
    
    // Show loading state
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline';
    submitBtn.disabled = true;
    
    // Simulate login process (replace with actual AJAX call)
    setTimeout(() => {
        // Check if it's a demo account
        if ((email === 'teacher@demo.com' || email === 'student@demo.com') && password === 'demo123') {
            showMessage('Login successful! Redirecting...', 'success');
            
            // Redirect after successful login
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1500);
        } else {
            showMessage('Invalid email or password. Please try again.', 'error');
            
            // Reset form and UI
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
            submitBtn.disabled = false;
        }
    }, 2000);
}

function handleSocialLogin(platform) {
    showMessage(`Redirecting to ${platform} authentication...`, 'info');
    
    // Simulate social login redirect
    setTimeout(() => {
        showMessage(`${platform} login would normally redirect to authentication service.`, 'info');
    }, 1000);
}

// Show message function
function showMessage(message, type) {
    // Remove existing messages
    const existingMessage = document.querySelector('.login-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create message element
    const messageEl = document.createElement('div');
    messageEl.className = `login-message login-message-${type}`;
    messageEl.textContent = message;
    
    // Add styles
    messageEl.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#d4edda' : type === 'error' ? '#f8d7da' : '#d1ecf1'};
        color: ${type === 'success' ? '#155724' : type === 'error' ? '#721c24' : '#0c5460'};
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        z-index: 1000;
        max-width: 300px;
        border-left: 4px solid ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(messageEl);
    
    // Remove message after 5 seconds
    setTimeout(() => {
        if (messageEl.parentNode) {
            messageEl.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (messageEl.parentNode) {
                    messageEl.remove();
                }
            }, 300);
        }
    }, 5000);
}

// Add CSS animations for messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (!hamburger.contains(e.target) && !navLinks.contains(e.target) && navLinks.classList.contains('open')) {
        hamburger.classList.remove('active');
        navLinks.classList.remove('open');
    }
});

// Enter key support for form submission
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const focused = document.activeElement;
        if (focused && focused.form && focused.form.id === 'login-form') {
            if (focused.type !== 'submit') {
                e.preventDefault();
                focused.form.dispatchEvent(new Event('submit'));
            }
        }
    }
});