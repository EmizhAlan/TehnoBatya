// Управление мобильным меню
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    const mobileMenuClose = document.querySelector('.mobile-menu-close');
    const body = document.body;

    // Открытие меню
    menuToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        mobileMenu.classList.toggle('active');
        body.classList.toggle('menu-open');
    });

    // Закрытие меню по кнопке
    mobileMenuClose.addEventListener('click', function() {
        menuToggle.classList.remove('active');
        mobileMenu.classList.remove('active');
        body.classList.remove('menu-open');
    });

    // Закрытие меню по клику на ссылку
    const mobileNavLinks = document.querySelectorAll('.mobile-nav a');
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', function() {
            menuToggle.classList.remove('active');
            mobileMenu.classList.remove('active');
            body.classList.remove('menu-open');
        });
    });

    // Закрытие меню по клику вне меню
    document.addEventListener('click', function(event) {
        if (mobileMenu.classList.contains('active') && 
            !mobileMenu.contains(event.target) && 
            !menuToggle.contains(event.target)) {
            menuToggle.classList.remove('active');
            mobileMenu.classList.remove('active');
            body.classList.remove('menu-open');
        }
    });

    // Закрытие меню при нажатии Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && mobileMenu.classList.contains('active')) {
            menuToggle.classList.remove('active');
            mobileMenu.classList.remove('active');
            body.classList.remove('menu-open');
        }
    });

    // Обработка переключения темы в мобильном меню
    const mobileThemeSwitcher = document.getElementById('mobile-theme-switcher');
    const mainThemeSwitcher = document.getElementById('theme-switcher');
    
    if (mobileThemeSwitcher && mainThemeSwitcher) {
        mobileThemeSwitcher.addEventListener('change', function() {
            mainThemeSwitcher.checked = this.checked;
            mainThemeSwitcher.dispatchEvent(new Event('change'));
        });
        
        mainThemeSwitcher.addEventListener('change', function() {
            mobileThemeSwitcher.checked = this.checked;
        });
    }
});