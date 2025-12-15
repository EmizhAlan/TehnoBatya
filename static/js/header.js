document.addEventListener('DOMContentLoaded', function() {
    // Мобильное меню
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            navMenu.classList.toggle('active');
            
            // Блокировка скролла при открытом меню
            if (navMenu.classList.contains('active')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });
        
        // Закрыть меню при клике на ссылку
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                menuToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
        
        // Выпадающее меню для мобильных
        const dropdowns = document.querySelectorAll('.dropdown');
        dropdowns.forEach(dropdown => {
            const link = dropdown.querySelector('.nav-link');
            
            link.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    dropdown.classList.toggle('active');
                    
                    // Закрыть другие открытые меню
                    dropdowns.forEach(other => {
                        if (other !== dropdown) {
                            other.classList.remove('active');
                        }
                    });
                }
            });
        });
        
        // Закрыть меню при клике вне его
        document.addEventListener('click', function(e) {
            if (!navMenu.contains(e.target) && !menuToggle.contains(e.target)) {
                menuToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
                
                // Закрыть все выпадающие меню
                dropdowns.forEach(dropdown => {
                    dropdown.classList.remove('active');
                });
            }
        });
    }
    
    // Эффект скролла для навигации
    const mainNav = document.querySelector('.main-nav');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            mainNav.style.boxShadow = '0 5px 25px rgba(0, 0, 0, 0.1)';
        } else {
            mainNav.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        }
    });
});

// Переключатель темы
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    // Проверяем сохраненную тему или системные настройки
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Устанавливаем начальную тему
    if (savedTheme === 'light' || (!savedTheme && !prefersDark)) {
        body.classList.add('light-theme');
        body.classList.remove('dark-theme');
    } else {
        body.classList.add('dark-theme');
        body.classList.remove('light-theme');
    }
    
    // Обработчик клика по переключателю
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            if (body.classList.contains('dark-theme')) {
                // Переключаем на светлую тему
                body.classList.remove('dark-theme');
                body.classList.add('light-theme');
                localStorage.setItem('theme', 'light');
            } else {
                // Переключаем на темную тему
                body.classList.remove('light-theme');
                body.classList.add('dark-theme');
                localStorage.setItem('theme', 'dark');
            }
        });
    }
    
    // Слушаем изменения системной темы
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            if (e.matches) {
                body.classList.add('dark-theme');
                body.classList.remove('light-theme');
            } else {
                body.classList.remove('dark-theme');
                body.classList.add('light-theme');
            }
        }
    });
});