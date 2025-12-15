import sys
import os
import random
from datetime import datetime, timedelta

# Добавляем текущую директорию в путь Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Review

def add_test_reviews():
    with app.app_context():
        # Очищаем существующие отзывы (опционально)
        db.session.query(Review).delete()
        
        # Создаем тестовые отзывы
        test_reviews = [
            {
                'author': 'Иван Петров',
                'position': 'Директор IT-компании',
                'text': 'Отличный сервис! Починили ноутбук за 2 часа, дали гарантию. Рекомендую!',
                'rating': 5,
                'service': 'Ремонт ноутбуков',
                'created_at': datetime.utcnow() - timedelta(days=2)
            },
            {
                'author': 'Мария Смирнова',
                'position': 'Бухгалтер',
                'text': 'Проходила курсы компьютерной грамотности. Преподаватели отличные, всё объясняют понятно.',
                'rating': 5,
                'service': 'Курсы',
                'created_at': datetime.utcnow() - timedelta(days=5)
            },
            {
                'author': 'Алексей Козлов',
                'position': 'Студент',
                'text': 'Собрали игровой компьютер по моему бюджету. Всё работает идеально, спасибо!',
                'rating': 5,
                'service': 'Сборка ПК',
                'created_at': datetime.utcnow() - timedelta(days=7)
            },
            {
                'author': 'Ольга Николаева',
                'position': 'Дизайнер',
                'text': 'Настроили Wi-Fi роутер, теперь интернет работает во всей квартире. Быстро и качественно.',
                'rating': 4,
                'service': 'Настройка сетей',
                'created_at': datetime.utcnow() - timedelta(days=10)
            },
            {
                'author': 'Дмитрий Соколов',
                'position': 'Предприниматель',
                'text': 'Консультация по выбору сервера для бизнеса помогла сэкономить бюджет. Спасибо!',
                'rating': 5,
                'service': 'Консультации',
                'created_at': datetime.utcnow() - timedelta(days=12)
            },
            {
                'author': 'Елена Воробьева',
                'position': 'Пенсионер',
                'text': 'Научили пользоваться компьютером с нуля. Очень терпеливые преподаватели, всем довольна.',
                'rating': 5,
                'service': 'Курсы',
                'created_at': datetime.utcnow() - timedelta(days=15)
            },
            {
                'author': 'Сергей Иванов',
                'position': 'Системный администратор',
                'text': 'Восстановили данные с поврежденного жесткого диска. Спасли важные рабочие файлы!',
                'rating': 5,
                'service': 'Ремонт ПК',
                'created_at': datetime.utcnow() - timedelta(days=20)
            },
            {
                'author': 'Анна Кузнецова',
                'position': 'Фотограф',
                'text': 'Починили MacBook после залития. Работает как новый, очень благодарна мастерам.',
                'rating': 4,
                'service': 'Ремонт ноутбуков',
                'created_at': datetime.utcnow() - timedelta(days=25)
            }
        ]
        
        for i, review_data in enumerate(test_reviews):
            review = Review(
                author=review_data['author'],
                position=review_data['position'],
                text=review_data['text'],
                rating=review_data['rating'],
                service=review_data['service'],
                created_at=review_data['created_at'],
                avatar_url=f'https://i.pravatar.cc/100?img={i+1}'  # Разные аватары
            )
            db.session.add(review)
        
        db.session.commit()
        print(f'✅ Добавлено {len(test_reviews)} тестовых отзывов')
        print(f'📊 База данных: {app.config["SQLALCHEMY_DATABASE_URI"]}')

if __name__ == '__main__':
    add_test_reviews()