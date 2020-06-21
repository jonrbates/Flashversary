# -*- coding: utf-8 -*-
from app import application
import random
import csv
from datetime import datetime
from flask import render_template, flash, redirect, url_for, session, request
from sqlalchemy.sql import func
from app.forms import (FlashcardForm,
                       LoginForm,
                       RegistrationForm,
                       )
from app.models import User, Flashcard
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@application.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'Flashcard': Flashcard}


def make_flashcards(user):
    """
    Populate Flashcard table for user.
    """
    with open('data/arithmetic.tsv', 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for prompt, response in csvreader:
            db.session.add(Flashcard(prompt=prompt,
                                     response=response,
                                     student=user))
    db.session.commit()


def select_card(eps=0.2):
    """Select card from db with exploration or exploitation.
    Use eps-greedy bandits.
    """
    if random.random() < eps:
        # explore
        card = current_user.flashcards.order_by(func.random()).first()
        print('explore')
    else:
        # exploit
        # choose max qval
        card = current_user.flashcards\
                .order_by(Flashcard.qval.desc(), Flashcard.timestamp)\
                .first()
    card.timestamp = datetime.utcnow()
    return card


def generate_alternative_numeric_response(card):
    """
    Generate alternative response from response r
    """
    # TODO: generative policy
    correct_response = int(card.response)
    return random.choice([str(correct_response+offset)
                         for offset in [-3, -2, -1, 1, 2, 3]
                         if correct_response+offset > 0])


def generate_responses(card):
    """
    Generate alternative responses and shuffle.
    """
    alternative_response = generate_alternative_numeric_response(card)
    responses = [card.response, alternative_response]
    i = random.sample(range(len(responses)), len(responses))
    return i, responses


def clear_card():
    """
    Clear current card from session.
    """
    session.pop('cardId', None)
    session.pop('i', None)
    session.pop('responses', None)


def evaluate_and_update(card, i, flashcard_form):
    if (flashcard_form.r1.data and i[0] == 0) \
            or (flashcard_form.r2.data and i[1] == 0):
        card.successes += 1
        reward = 0
    else:
        # adversary wins a reward
        reward = 1
    card.attempts += 1
    card.qval = card.qval + (reward - card.qval) / card.attempts
    db.session.add(card)
    db.session.commit()
    if reward == 1:
        session['runLength'] = 0
        flash(session['runLength'], "warning")
    else:
        session['runLength'] += 1
        flash(session['runLength'], "success")
    clear_card()


def continue_or_generate_session():
    # draw card if needed
    if 'cardId' not in session:
        card = select_card()
        i, responses = generate_responses(card)
        session['cardId'] = card.id
        session['i'] = i
        session['responses'] = responses
    return session['cardId'], session['i'], session['responses']


@application.route('/index')
@application.route('/', methods=['GET', 'POST'])
@login_required
def index():
    session['showTable'] = session.get('showTable', False)
    session['runLength'] = session.get('runLength', 0)
    flashcard_form = FlashcardForm()
    card_id, i, responses = continue_or_generate_session()
    card = Flashcard.query.get(card_id)
    # write responses on buttons
    flashcard_form.r1.label.text = responses[i[0]]
    flashcard_form.r2.label.text = responses[i[1]]
    if flashcard_form.validate_on_submit():
        evaluate_and_update(card, i, flashcard_form)
        return redirect(url_for('index'))

    if session['showTable']:
        head_cards = current_user.flashcards\
                        .order_by(Flashcard.qval.desc(), Flashcard.timestamp)\
                        .limit(10).all()
    else:
        head_cards = []

    return render_template('index.html',
                           flask_debug=application.debug,
                           flashcard_form=flashcard_form,
                           card=card,
                           head_cards=head_cards)


@application.route('/toggle_table')
@login_required
def toggle_table():
    session['showTable'] = not session['showTable'] if 'showTable' in session \
        else False
    return redirect(url_for('index'))


@application.route('/draw_card')
@login_required
def draw_card():
    clear_card()
    return redirect(url_for('index'))


@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=True)    # form.remember_me.data
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@application.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        make_flashcards(user)
        flash('Congratulations, you are now a registered user!', 'info')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@application.route('/edit')
@login_required
def edit():
    flash("Warning: Do not include sensitive information.")
    return
