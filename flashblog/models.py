from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from flashblog import db, login_manager
from flask_login import UserMixin
import secrets

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )
    image_file = db.Column(
        db.String(20),
        nullable=False,
        default='default.jpg'
    )
    password = db.Column(
        db.String(60),
        nullable=False
    )
    posts = db.relationship(
        'Post',
        backref='author',
        lazy=True
    )
    files = db.relationship(
        'File',
        backref='owner',
        lazy=True
    )
    folders = db.relationship(
        'Folder',
        backref='owner',
        lazy=True
    )
    def get_reset_token(self):
        s = Serializer(
            current_app.config['SECRET_KEY']
        )
        return s.dumps(
            {'user_id': self.id}
        )
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(
            current_app.config['SECRET_KEY']
        )
        try:
            user_id = s.loads(
                token,
                max_age=1800
            )['user_id']
        except Exception:
            return None
        return User.query.get(user_id)
    def __repr__(self):
        return (
            f"User('{self.username}',"
            f"'{self.email}',"
            f"'{self.image_file}')"
        )


@staticmethod
def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token, max_age=1800)['user_id']
    except Exception:
        return None
    return User.query.get(user_id)
def __repr__(self):
    return f"User('{self.username}','{self.email}','{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}')"


class Folder(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    files = db.relationship(
        'File',
        backref='folder',
        lazy=True
    )
    def __repr__(self):
        return f"Folder('{self.name}')"


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    size = db.Column(db.Integer, default=0)
    upload_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    folder_id = db.Column(
        db.Integer,
        db.ForeignKey('folder.id'),
        nullable=True
    )
    is_deleted = db.Column(
        db.Boolean,
        default=False
    )
    def __repr__(self):
     return f"File('{self.filename}')"

class SharedFile(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    token = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    file_id = db.Column(
        db.Integer,
        db.ForeignKey('file.id'),
        nullable=False
    )
    def __repr__(self):
     return f"SharedFile('{self.token}')"

