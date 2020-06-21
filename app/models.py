# -*- coding: utf-8 -*-
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    flashcards = db.relationship('Flashcard', backref='student', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    prompt = db.Column(db.String(4096))
    response = db.Column(db.String(512))
    successes = db.Column(db.Integer, default=0)
    attempts = db.Column(db.Integer, default=0)
    qval = db.Column(db.Float, default=1., index=True)  # warm start
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def __repr__(self):
        return f'<{self.id}, {self.user_id}, {self.prompt},'\
                f' {self.attempts}, {self.successes}, {self.qval},'\
                f' {self.timestamp}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
