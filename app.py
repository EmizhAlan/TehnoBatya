from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
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

@app.route('/services/repair')
def repair():
    return render_template('repair.html', title='Ремонт ПК - Техно Батя')

@app.route('/services/network')
def network():
    return render_template('network.html', title='Сети - Техно Батя')

@app.route('/services/consulting')
def consulting():
    return render_template('consulting.html', title='Консультации - Техно Батя')

@app.route('/services/software')
def software():
    return render_template('software.html', title='Программы - Техно Батя')

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

if __name__ == '__main__':
    # Создаем необходимые папки, если они не существуют
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)