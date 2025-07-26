// ========================================================================
// MODERN SCIENTIFIC SALARY ANALYSIS WEBSITE JAVASCRIPT
// ========================================================================

// Data for charts and analysis
const salaryData = {
    regions: {
        'US': {
            name: 'Amerika Birleşik Devletleri',
            flag: '🇺🇸',
            averageSalary: 112431,
            medianSalary: 110000,
            gini: 0.268,
            records: 1363,
            experience: {
                entry: { salary: 49980, count: 275 },
                mid: { salary: 86154, count: 287 },
                senior: { salary: 144529, count: 794 }
            }
        },
        'TR': {
            name: 'Türkiye',
            flag: '🇹🇷',
            averageSalary: 5991,
            medianSalary: 6030,
            gini: 0.274,
            records: 1343,
            experience: {
                entry: { salary: 2638, count: 283 },
                mid: { salary: 4455, count: 267 },
                senior: { salary: 7783, count: 785 }
            }
        },
        'EU': {
            name: 'Avrupa Birliği',
            flag: '🇪🇺',
            averageSalary: 2770,
            medianSalary: 2122,
            gini: 0.451,
            records: 65,
            experience: {
                entry: { salary: 0, count: 0 },
                mid: { salary: 0, count: 0 },
                senior: { salary: 0, count: 0 }
            }
        }
    },
    comparisons: {
        'TR_vs_US': 19.07,
        'TR_vs_EU': 27.57,
        'EU_vs_US': 1.35
    }
};

// Chart configurations
const chartColors = {
    primary: '#2563eb',
    primaryLight: '#3b82f6',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#dc2626',
    gray: '#6b7280'
};

// DOM elements
const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initCharts();
    initScrollAnimations();
    initTabFunctionality();
    initMobileMenu();
});

// ========================================================================
// NAVIGATION FUNCTIONALITY
// ========================================================================

function initNavigation() {
    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerOffset = 80;
                const elementPosition = targetSection.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
                
                // Update active nav link
                updateActiveNavLink(this);
                
                // Close mobile menu if open
                if (navMenu.classList.contains('active')) {
                    toggleMobileMenu();
                }
            }
        });
    });
    
    // Update active nav link on scroll
    window.addEventListener('scroll', updateNavOnScroll);
    
    // Add navbar background on scroll
    window.addEventListener('scroll', updateNavbarBackground);
}

function updateActiveNavLink(activeLink) {
    navLinks.forEach(link => link.classList.remove('active'));
    activeLink.classList.add('active');
}

function updateNavOnScroll() {
    const sections = document.querySelectorAll('section[id]');
    const scrollPos = window.scrollY + 100;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');
        
        if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            const correspondingNavLink = document.querySelector(`a[href="#${sectionId}"]`);
            if (correspondingNavLink) {
                updateActiveNavLink(correspondingNavLink);
            }
        }
    });
}

function updateNavbarBackground() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
}

// ========================================================================
// MOBILE MENU FUNCTIONALITY
// ========================================================================

function initMobileMenu() {
    if (navToggle) {
        navToggle.addEventListener('click', toggleMobileMenu);
    }
}

function toggleMobileMenu() {
    navMenu.classList.toggle('active');
    navToggle.classList.toggle('active');
    
    // Animate hamburger bars
    const bars = navToggle.querySelectorAll('.bar');
    bars.forEach((bar, index) => {
        if (navToggle.classList.contains('active')) {
            if (index === 0) bar.style.transform = 'rotate(45deg) translate(5px, 5px)';
            if (index === 1) bar.style.opacity = '0';
            if (index === 2) bar.style.transform = 'rotate(-45deg) translate(7px, -6px)';
        } else {
            bar.style.transform = 'none';
            bar.style.opacity = '1';
        }
    });
}

// ========================================================================
// CHART FUNCTIONALITY
// ========================================================================

function initCharts() {
    createHeroChart();
    createMainChart();
}

function createHeroChart() {
    const ctx = document.getElementById('heroChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['ABD', 'Türkiye', 'AB'],
            datasets: [{
                data: [
                    salaryData.regions.US.averageSalary,
                    salaryData.regions.TR.averageSalary,
                    salaryData.regions.EU.averageSalary
                ],
                backgroundColor: [
                    chartColors.primary,
                    chartColors.success,
                    chartColors.warning
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: 'white',
                        font: {
                            size: 12,
                            weight: '600'
                        },
                        padding: 20
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': $' + context.parsed.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

function createMainChart() {
    const ctx = document.getElementById('mainChart');
    if (!ctx) return;
    
    // Default chart - Salary Comparison
    createSalaryComparisonChart(ctx);
}

function createSalaryComparisonChart(ctx) {
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['ABD 🇺🇸', 'Türkiye 🇹🇷', 'AB 🇪🇺'],
            datasets: [
                {
                    label: 'Ortalama Maaş ($)',
                    data: [
                        salaryData.regions.US.averageSalary,
                        salaryData.regions.TR.averageSalary,
                        salaryData.regions.EU.averageSalary
                    ],
                    backgroundColor: [
                        chartColors.primary,
                        chartColors.success,
                        chartColors.warning
                    ],
                    borderRadius: 8,
                    borderSkipped: false
                },
                {
                    label: 'Medyan Maaş ($)',
                    data: [
                        salaryData.regions.US.medianSalary,
                        salaryData.regions.TR.medianSalary,
                        salaryData.regions.EU.medianSalary
                    ],
                    backgroundColor: [
                        chartColors.primaryLight,
                        '#34d399',
                        '#fbbf24'
                    ],
                    borderRadius: 8,
                    borderSkipped: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': $' + context.parsed.y.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

function createGiniChart(ctx) {
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Gelir Adaleti', 'Veri Kalitesi', 'Ekonomik Performans', 'Sosyal Denge', 'Gelişmişlik'],
            datasets: [
                {
                    label: 'ABD 🇺🇸',
                    data: [95, 98, 95, 92, 95], // Normalized scores
                    borderColor: chartColors.primary,
                    backgroundColor: chartColors.primary + '20',
                    pointBackgroundColor: chartColors.primary,
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: chartColors.primary
                },
                {
                    label: 'Türkiye 🇹🇷',
                    data: [92, 85, 45, 88, 70],
                    borderColor: chartColors.success,
                    backgroundColor: chartColors.success + '20',
                    pointBackgroundColor: chartColors.success,
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: chartColors.success
                },
                {
                    label: 'AB 🇪🇺',
                    data: [55, 60, 60, 65, 85],
                    borderColor: chartColors.warning,
                    backgroundColor: chartColors.warning + '20',
                    pointBackgroundColor: chartColors.warning,
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: chartColors.warning
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: {
                        display: true
                    },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            weight: '600'
                        }
                    }
                }
            }
        }
    });
}

function createExperienceChart(ctx) {
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Entry Level', 'Mid Level', 'Senior'],
            datasets: [
                {
                    label: 'ABD 🇺🇸',
                    data: [
                        salaryData.regions.US.experience.entry.salary,
                        salaryData.regions.US.experience.mid.salary,
                        salaryData.regions.US.experience.senior.salary
                    ],
                    borderColor: chartColors.primary,
                    backgroundColor: chartColors.primary + '10',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointHoverRadius: 8
                },
                {
                    label: 'Türkiye 🇹🇷',
                    data: [
                        salaryData.regions.TR.experience.entry.salary,
                        salaryData.regions.TR.experience.mid.salary,
                        salaryData.regions.TR.experience.senior.salary
                    ],
                    borderColor: chartColors.success,
                    backgroundColor: chartColors.success + '10',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': $' + context.parsed.y.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

// ========================================================================
// TAB FUNCTIONALITY
// ========================================================================

function initTabFunctionality() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const chartCanvas = document.getElementById('mainChart');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Get chart type
            const chartType = this.getAttribute('data-chart');
            
            // Destroy existing chart and create new one
            if (chartCanvas) {
                const existingChart = Chart.getChart(chartCanvas);
                if (existingChart) {
                    existingChart.destroy();
                }
                
                // Create appropriate chart based on tab
                switch(chartType) {
                    case 'salary-comparison':
                        createSalaryComparisonChart(chartCanvas);
                        break;
                    case 'gini-analysis':
                        createGiniChart(chartCanvas);
                        break;
                    case 'experience-breakdown':
                        createExperienceChart(chartCanvas);
                        break;
                }
            }
        });
    });
}

// ========================================================================
// SCROLL ANIMATIONS
// ========================================================================

function initScrollAnimations() {
    // Add scroll reveal class to elements
    const revealElements = document.querySelectorAll(
        '.finding-card, .analysis-block, .method-card, .insight-card, .comparison-card'
    );
    
    revealElements.forEach(el => {
        el.classList.add('scroll-reveal');
    });
    
    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    revealElements.forEach(el => {
        observer.observe(el);
    });
    
    // Counter animation for statistics
    animateCounters();
}

function animateCounters() {
    const counters = document.querySelectorAll('.stat-number, .metric');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.5
    });
    
    counters.forEach(counter => {
        observer.observe(counter);
    });
}

function animateCounter(element) {
    const text = element.textContent;
    const hasComma = text.includes(',');
    const hasDollar = text.includes('$');
    const hasDecimal = text.includes('.');
    
    let target = parseFloat(text.replace(/[$,]/g, ''));
    
    if (isNaN(target)) return;
    
    let current = 0;
    const increment = target / 100;
    const duration = 2000; // 2 seconds
    const stepTime = duration / 100;
    
    const timer = setInterval(() => {
        current += increment;
        
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        let displayValue = current;
        
        if (hasDecimal && target < 1) {
            displayValue = displayValue.toFixed(3);
        } else if (hasDecimal) {
            displayValue = displayValue.toFixed(2);
        } else {
            displayValue = Math.floor(displayValue);
        }
        
        let formattedValue = displayValue.toString();
        
        if (hasComma && displayValue >= 1000) {
            formattedValue = displayValue.toLocaleString();
        }
        
        if (hasDollar) {
            formattedValue = '$' + formattedValue;
        }
        
        element.textContent = formattedValue;
    }, stepTime);
}

// ========================================================================
// UTILITY FUNCTIONS
// ========================================================================

// Format currency
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Format percentage
function formatPercentage(value) {
    return (value * 100).toFixed(1) + '%';
}

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add debounced scroll listeners
window.addEventListener('scroll', debounce(updateNavOnScroll, 10));
window.addEventListener('scroll', debounce(updateNavbarBackground, 10));

// ========================================================================
// ADDITIONAL INTERACTIONS
// ========================================================================

// Add loading state management
function showLoading(element) {
    element.classList.add('loading');
}

function hideLoading(element) {
    element.classList.remove('loading');
}

// Add tooltip functionality for complex data
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = e.target.getAttribute('data-tooltip');
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// ========================================================================
// ERROR HANDLING AND PERFORMANCE
// ========================================================================

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Application error:', e.error);
    // You could send this to an analytics service
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
        }, 0);
    });
}

// Check for reduced motion preference
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

if (prefersReducedMotion.matches) {
    // Disable animations for users who prefer reduced motion
    document.documentElement.style.setProperty('--animation-duration', '0s');
}

// Print functionality
function printReport() {
    window.print();
}

// Export functionality (if needed)
function exportToPDF() {
    // This would require a PDF library like jsPDF
    console.log('PDF export functionality would be implemented here');
}

// Initialize tooltips on load
document.addEventListener('DOMContentLoaded', initTooltips);

// Add keyboard navigation support
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        // Close mobile menu if open
        if (navMenu && navMenu.classList.contains('active')) {
            toggleMobileMenu();
        }
    }
});

// Focus management for accessibility
function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
        'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
    );
    
    const firstFocusableElement = focusableElements[0];
    const lastFocusableElement = focusableElements[focusableElements.length - 1];
    
    element.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstFocusableElement) {
                    lastFocusableElement.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastFocusableElement) {
                    firstFocusableElement.focus();
                    e.preventDefault();
                }
            }
        }
    });
}