
document.addEventListener('DOMContentLoaded', function() {
    console.log('Teacher Profile Detail page loaded');
    
    
    const resourceSections = document.querySelectorAll('.resource-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    resourceSections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
    
    // Add download/watch button animations
    const actionButtons = document.querySelectorAll('.btn-download, .btn-watch');
    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add click feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
    
    // Resource item hover effects
    const resourceItems = document.querySelectorAll('.resource-item');
    resourceItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.boxShadow = 'none';
        });
    });
    
   
    const resourceLists = document.querySelectorAll('.resource-list');
    resourceLists.forEach(list => {
        if (list.scrollHeight > list.clientHeight) {
            list.scrollTop = list.scrollHeight;
        }
    });
});


const scrollbarStyle = document.createElement('style');
scrollbarStyle.textContent = `
    .resource-list::-webkit-scrollbar {
        width: 6px;
    }
    
    .resource-list::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    
    .resource-list::-webkit-scrollbar-thumb {
        background: #A02A2D;
        border-radius: 3px;
    }
    
    .resource-list::-webkit-scrollbar-thumb:hover {
        background: #7E1D21;
    }
`;
document.head.appendChild(scrollbarStyle);