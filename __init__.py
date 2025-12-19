from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
import re
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'technobatya-secret-key'

# Убедитесь, что Flask ищет шаблоны в правильной папке
app.template_folder = 'templates'

# Настройка базы данных
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "reviews.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Измените на случайный ключ

# Инициализация базы данных
db = SQLAlchemy(app)

# Модель для отзывов
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))  # Должность/описание автора
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 звезд
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=True)
    avatar_url = db.Column(db.String(200), default='https://i.pravatar.cc/100')
    service = db.Column(db.String(100))  # Услуга, по которой оставлен отзыв
    
    def __repr__(self):
        return f'<Review {self.author}>'

# Создаем таблицы при запуске
with app.app_context():
    db.create_all()


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Страница курсов
@app.route('/courses')
def courses():
    courses_list = [
        {'id': 1, 'name': 'Программирование на Python', 'duration': '3 месяца', 'price': '15 000 ₽'},
        {'id': 2, 'name': 'Веб-разработка', 'duration': '4 месяца', 'price': '20 000 ₽'},
        {'id': 3, 'name': 'Компьютерная грамотность', 'duration': '2 месяца', 'price': '8 000 ₽'},
        {'id': 4, 'name': 'Кибербезопасность', 'duration': '3 месяца', 'price': '18 000 ₽'},
        {'id': 5, 'name': 'Графический дизайн', 'duration': '3 месяца', 'price': '16 000 ₽'},
        {'id': 6, 'name': 'Мобильная разработка', 'duration': '4 месяца', 'price': '22 000 ₽'},
    ]
    return render_template('courses.html', courses=courses_list)

# Страница "О нас"
@app.route('/about')
def about():
    return render_template('about.html')

# Страница контактов
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        flash('Сообщение отправлено! Мы свяжемся с вами в ближайшее время.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# Запись на курс
@app.route('/enroll', methods=['POST'])
def enroll():
    if request.method == 'POST':
        course_id = request.form['course_id']
        student_name = request.form['student_name']
        phone = request.form['phone']
        
        flash('Вы успешно записались на курс!', 'success')
        return redirect(url_for('courses'))

# Страница 404 (если страница не найдена)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Добавьте эти маршруты
@app.route('/services')
def services():
    return render_template('services.html', title='Услуги - Техно Батя')

@app.route('/repair')
@app.route('/services/repair')
def repair():
    return render_template('repair.html', title='Ремонт ПК - Техно Батя')

@app.route('/services/network')
def network():
    return render_template('network.html', title='Сети - Техно Батя')

@app.route('/services/consulting')
def consulting():
    return render_template('consulting.html', title='Консультации - Техно Батя')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', title='Портфолио - Техно Батя')

@app.route('/team')
def team():
    return render_template('team.html', title='Команда - Техно Батя')

# Страница отзывов
@app.route('/reviews')
def reviews():
    # Получаем все одобренные отзывы, отсортированные по дате
    reviews_list = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).all()
    return render_template('reviews.html', reviews=reviews_list, title='Отзывы - Техно Батя')

# API для получения отзывов (для AJAX)
@app.route('/api/reviews')
def api_reviews():
    reviews_list = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).all()
    reviews_data = []
    for review in reviews_list:
        reviews_data.append({
            'id': review.id,
            'author': review.author,
            'position': review.position,
            'text': review.text,
            'rating': review.rating,
            'created_at': review.created_at.strftime('%d.%m.%Y'),
            'avatar_url': review.avatar_url,
            'service': review.service
        })
    return jsonify(reviews_data)

# Добавление нового отзыва
@app.route('/api/reviews/add', methods=['POST'])
def add_review():
    try:
        data = request.get_json()
        
        new_review = Review(
            author=data['author'],
            position=data.get('position', 'Клиент'),
            text=data['text'],
            rating=data['rating'],
            avatar_url=data.get('avatar_url', f'https://i.pravatar.cc/100?img={random.randint(1, 70)}'),
            service=data.get('service', 'Общая услуга')
        )
        
        db.session.add(new_review)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Отзыв успешно добавлен и будет опубликован после модерации!',
            'review_id': new_review.id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка при добавлении отзыва: {str(e)}'
        }), 400

# Статистика отзывов
@app.route('/api/reviews/stats')
def reviews_stats():
    total = Review.query.filter_by(is_approved=True).count()
    avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(is_approved=True).scalar() or 0
    recent = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).limit(5).count()
    
    return jsonify({
        'total': total,
        'avg_rating': round(avg_rating, 1),
        'recent': recent
    })
    
@app.route('/api/repair/request', methods=['POST'])
def repair_request():
    try:
        # Получаем данные из формы
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        device_type = request.form.get('device_type', '').strip()
        brand = request.form.get('brand', '').strip()
        problem_type = request.form.get('problem_type', '').strip()
        problem_description = request.form.get('problem_description', '').strip()
        call_master = request.form.get('call_master') == 'on'
        
        # Валидация данных
        if not name or not phone or not device_type or not problem_type or not problem_description:
            return jsonify({
                'success': False,
                'message': 'Пожалуйста, заполните все обязательные поля'
            })
        
        # Валидация телефона (простая проверка)
        phone_pattern = r'^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$'
        if not re.match(phone_pattern, phone):
            return jsonify({
                'success': False,
                'message': 'Пожалуйста, введите корректный номер телефона'
            })
        
        # Здесь можно добавить логику сохранения заявки в базу данных
        # Например, создать модель RepairRequest
        
        # Пока просто возвращаем успешный ответ
        master_text = "с выездом мастера" if call_master else "в сервисном центре"
        response_message = (
            f"Заявка на ремонт принята!\n\n"
            f"Имя: {name}\n"
            f"Телефон: {phone}\n"
            f"Устройство: {device_type} ({brand if brand else 'бренд не указан'})\n"
            f"Проблема: {problem_type}\n\n"
            f"Мастер свяжется с вами в течение 15 минут для уточнения деталей.\n"
            f"Ремонт будет выполнен {master_text}."
        )
        
        # В реальном приложении здесь можно:
        # 1. Сохранить заявку в базу данных
        # 2. Отправить уведомление на почту
        # 3. Отправить SMS менеджеру
        # 4. Интегрировать с CRM системой
        
        return jsonify({
            'success': True,
            'message': response_message
        })
        
    except Exception as e:
        print(f"Ошибка при обработке заявки: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка при обработке заявки. Пожалуйста, попробуйте позже.'
        }), 500
        
@app.route('/network')
def network_redirect():
    return redirect(url_for('network'))

@app.route('/consulting')
def consulting_route():
    return render_template('consulting.html', title='Консультации - Техно Батя')

@app.route('/software')
@app.route('/services/software')
def software():
    return render_template('software.html', title='Программы - Техно Батя')

@app.route('/api/consulting/request', methods=['POST'])
def consulting_request():
    try:
        # Получаем данные из формы
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        company = request.form.get('company', '').strip()
        consultation_type = request.form.get('consultation_type', '').strip()
        preferred_date = request.form.get('preferred_date', '').strip()
        format_type = request.form.get('format', '').strip()
        problem_description = request.form.get('problem_description', '').strip()
        receive_newsletter = request.form.get('receive_newsletter') == 'on'
        agree_terms = request.form.get('agree_terms') == 'on'
        
        # Валидация данных
        required_fields = ['name', 'phone', 'email', 'consultation_type', 'format', 'problem_description']
        for field in required_fields:
            if not locals()[field]:
                return jsonify({
                    'success': False,
                    'message': f'Пожалуйста, заполните поле: {field}'
                })
        
        if not agree_terms:
            return jsonify({
                'success': False,
                'message': 'Необходимо согласие с политикой конфиденциальности'
            })
        
        # Валидация email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({
                'success': False,
                'message': 'Пожалуйста, введите корректный email'
            })
        
        # Валидация телефона
        phone_pattern = r'^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$'
        if not re.match(phone_pattern, phone):
            return jsonify({
                'success': False,
                'message': 'Пожалуйста, введите корректный номер телефона'
            })
        
        # Типы консультаций
        consultation_types = {
            'business': 'Бизнес-консультация',
            'personal': 'Персональная консультация',
            'technical': 'Техническая экспертиза',
            'not_sure': 'Помощь в выборе консультации'
        }
        
        # Форматы консультаций
        formats = {
            'online': 'Онлайн',
            'offline': 'Очно в офисе',
            'both': 'Любой формат'
        }
        
        # Формирование ответа
        response_message = (
            f"Заявка на консультацию принята!\n\n"
            f"Имя: {name}\n"
            f"Телефон: {phone}\n"
            f"Email: {email}\n"
            f"Компания: {company if company else 'не указана'}\n"
            f"Тип консультации: {consultation_types.get(consultation_type, consultation_type)}\n"
            f"Формат: {formats.get(format_type, format_type)}\n"
            f"Предпочтительное время: {preferred_date if preferred_date else 'не указано'}\n\n"
            f"Наш эксперт свяжется с вами в течение 2 часов для бесплатной 15-минутной консультации.\n"
            f"Мы обсудим вашу задачу: {problem_description[:100]}..."
        )
        
        return jsonify({
            'success': True,
            'message': response_message
        })
        
    except Exception as e:
        print(f"Ошибка при обработке заявки: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка при обработке заявки. Пожалуйста, попробуйте позже.'
        }), 500
        
@app.route('/api/software/request', methods=['POST'])
def software_request():
    try:
        # Получаем данные из формы
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        device_count = request.form.get('device_count', '').strip()
        software_type = request.form.get('software_type', '').strip()
        installation_type = request.form.get('installation_type', '').strip()
        problem_description = request.form.get('problem_description', '').strip()
        need_licenses = request.form.get('need_licenses') == 'on'
        need_training = request.form.get('need_training') == 'on'
        agree_terms = request.form.get('agree_terms') == 'on'
        
        # Собираем выбранные программы
        selected_software = []
        if request.form.get('software_ms_office') == 'on':
            selected_software.append('Microsoft Office')
        if request.form.get('software_antivirus') == 'on':
            selected_software.append('Антивирусы')
        if request.form.get('software_adobe') == 'on':
            selected_software.append('Adobe Creative Cloud')
        if request.form.get('software_development') == 'on':
            selected_software.append('Инструменты разработки')
        if request.form.get('software_other') == 'on':
            selected_software.append('Другое ПО')
        
        # Валидация данных
        required_fields = ['name', 'phone', 'software_type', 'installation_type', 'problem_description']
        for field in required_fields:
            if not locals()[field]:
                return jsonify({
                    'success': False,
                    'message': f'Пожалуйста, заполните поле: {field}'
                })
        
        if not agree_terms:
            return jsonify({
                'success': False,
                'message': 'Необходимо согласие с политикой конфиденциальности'
            })
        
        # Валидация телефона
        phone_pattern = r'^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$'
        if not re.match(phone_pattern, phone):
            return jsonify({
                'success': False,
                'message': 'Пожалуйста, введите корректный номер телефона'
            })
        
        # Типы ПО
        software_types = {
            'office': 'Офисные программы',
            'security': 'Антивирусы и безопасность',
            'creative': 'Графические редакторы',
            'development': 'Инструменты разработки',
            'multiple': 'Несколько типов',
            'other': 'Другое'
        }
        
        # Типы установки
        installation_types = {
            'remote': 'Удаленная установка',
            'onsite': 'Выезд специалиста',
            'both': 'Любой тип'
        }
        
        # Формирование ответа
        software_list = ', '.join(selected_software) if selected_software else 'не указаны'
        licenses_text = 'нужна помощь с лицензиями' if need_licenses else 'без помощи с лицензиями'
        training_text = 'с обучением' if need_training else 'без обучения'
        
        response_message = (
            f"Заявка на установку ПО принята!\n\n"
            f"Имя: {name}\n"
            f"Телефон: {phone}\n"
            f"Email: {email if email else 'не указан'}\n"
            f"Количество устройств: {device_count if device_count else 'не указано'}\n"
            f"Тип ПО: {software_types.get(software_type, software_type)}\n"
            f"Выбранные программы: {software_list}\n"
            f"Тип установки: {installation_types.get(installation_type, installation_type)}\n"
            f"Дополнительно: {licenses_text}, {training_text}\n\n"
            f"Задача: {problem_description[:100]}...\n\n"
            f"Наш специалист свяжется с вами в течение часа для уточнения деталей."
        )
        
        return jsonify({
            'success': True,
            'message': response_message
        })
        
    except Exception as e:
        print(f"Ошибка при обработке заявки: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Произошла ошибка при обработке заявки. Пожалуйста, попробуйте позже.'
        }), 500

if __name__ == '__main__':
    # Создаем необходимые папки, если они не существуют
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)