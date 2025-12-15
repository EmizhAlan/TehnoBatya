from datetime import datetime

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