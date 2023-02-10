from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import db, login


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    updates = db.relationship('Updates', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()
        
    def __repr__(self):
        return f'<User {self.id}|{self.username}>'
    
    def check_password(self, attemptPass):
        return check_password_hash(self.password, attemptPass)
    
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Updates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Updates{self.id}|{self.user_id}>'
    
    def update(self, **kwargs):
        for key,value in kwargs.items():
            if key in {'body'}:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
