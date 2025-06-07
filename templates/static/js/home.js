// DOM Elements
const featureCards = document.querySelectorAll('.feature-card');
const stepCards = document.querySelectorAll('.step-card');
const foodCards = document.querySelectorAll('.food-card');
const pnrInput = document.querySelector('.pnr-input');
const pnrForm = document.querySelector('.pnr-form');

// Initialize animations when elements come into view
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
        }
    });
}, { threshold: 0.1 });

// Observe elements for animations
featureCards.forEach(card => observer.observe(card));
stepCards.forEach(step => observer.observe(step));
foodCards.forEach(card => observer.observe(card));

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            window.scrollTo({
                top: target.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// PNR form validation
if (pnrForm) {
    pnrForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const pnr = pnrInput.value.trim();
        
        if (pnr.length !== 10 || !/^\d+$/.test(pnr)) {
            alert('Please enter a valid 10-digit PNR number');
            return;
        }
        
        // Redirect to search page with PNR
        window.location.href = `/trains/search/?pnr=${pnr}`;
    });
}

// PNR options click handlers
document.querySelectorAll('.pnr-option').forEach(option => {
    option.addEventListener('click', function() {
        const type = this.querySelector('span').textContent.toLowerCase();
        window.location.href = `/trains/search/?type=${type}`;
    });
});

// Add click handlers for food cards
document.querySelectorAll('.food-card').forEach(card => {
    card.addEventListener('click', function() {
        const foodName = this.querySelector('h3').textContent;
        window.location.href = `/search/?food=${encodeURIComponent(foodName)}`;
    });
}); 