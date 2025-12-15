// Анимация кнопки "Наверх"
document.addEventListener('DOMContentLoaded', function() {
    // Кнопка "Наверх"
    const backToTopBtn = document.getElementById('backToTop');
    
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        // Показывать/скрывать кнопку при скролле
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopBtn.style.opacity = '1';
                backToTopBtn.style.visibility = 'visible';
                backToTopBtn.style.transform = 'translateY(0)';
            } else {
                backToTopBtn.style.opacity = '0';
                backToTopBtn.style.visibility = 'hidden';
                backToTopBtn.style.transform = 'translateY(10px)';
            }
        });
        
        // Изначально скрыта
        backToTopBtn.style.transition = 'all 0.3s ease';
        backToTopBtn.style.opacity = '0';
        backToTopBtn.style.visibility = 'hidden';
        backToTopBtn.style.transform = 'translateY(10px)';
    }
    
    // Анимация при наведении на ссылки
    const links = document.querySelectorAll('.col-links li a, .social-link');
    links.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });
    
    // Плавное появление элементов при скролле
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
            }
        });
    }, observerOptions);
    
    // Наблюдаем за анимированными элементами
    const animatedElements = document.querySelectorAll('.footer-top, .footer-middle, .footer-bottom');
    animatedElements.forEach(el => {
        observer.observe(el);
    });
    
    // Форма подписки
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = this.querySelector('input[type="email"]');
            const submitBtn = this.querySelector('button');
            
            if (emailInput.value) {
                // Анимация успешной отправки
                submitBtn.innerHTML = '<i class="fas fa-check"></i>';
                submitBtn.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
                
                setTimeout(() => {
                    submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
                    submitBtn.style.background = 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)';
                    emailInput.value = '';
                    
                    // Всплывающее уведомление
                    const notification = document.createElement('div');
                    notification.className = 'form-notification';
                    notification.innerHTML = 'Спасибо за подписку!';
                    notification.style.cssText = `
                        position: fixed;
                        top: 20px;
                        right: 20px;
                        background: #10b981;
                        color: white;
                        padding: 1rem 1.5rem;
                        border-radius: 8px;
                        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);
                        z-index: 1000;
                        animation: slideInRight 0.3s ease-out;
                    `;
                    
                    document.body.appendChild(notification);
                    
                    setTimeout(() => {
                        notification.style.animation = 'slideOutRight 0.3s ease-out forwards';
                        setTimeout(() => notification.remove(), 300);
                    }, 3000);
                }, 2000);
            }
        });
    }
    
    // Добавляем CSS для анимации уведомления
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOutRight {
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});