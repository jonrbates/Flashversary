# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User


class FlashcardForm(FlaskForm):
    r1 = SubmitField()
    r2 = SubmitField()


class AddFlashcardForm(FlaskForm):
    prompt = TextAreaField('prompt', validators=[DataRequired(), Length(min=0, max=4096)])
    response = TextAreaField('response', validators=[DataRequired(), Length(min=0, max=512)])
    submit = SubmitField('add flashcard')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')     # , validators=[DataRequired()]
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')    # , validators=[DataRequired()]
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
