// Открытие модального окна записи
function enrollCourse(courseId) {
    document.getElementById('courseId').value = courseId;
    document.getElementById('enrollModal').style.display = 'block';
}

// Закрытие модального окна
document.querySelectorAll('.close').forEach(closeBtn => {
    closeBtn.addEventListener('click', function() {
        this.closest('.modal').style.display = 'none';
    });
});

// Закрытие при клике вне окна
window.addEventListener('click', function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});

// Валидация формы
document.getElementById('enrollForm')?.addEventListener('submit', function(e) {
    const phone = document.getElementById('phone').value;
    const phoneRegex = /^[\+]?[7-8]?[0-9]{10}$/;
    
    if (!phoneRegex.test(phone.replace(/\D/g, ''))) {
        e.preventDefault();
        alert('Пожалуйста, введите корректный номер телефона');
    }
});