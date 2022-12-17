from app import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class SignupForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(),
        Length(min=3, max=100)
    ],
        render_kw={"placeholder": "Username", "class": "input is-large"})

    email = StringField(validators=[
        InputRequired(),
        Length(min=6, max=100)
    ],
        render_kw={"placeholder": "Email", "class": "input is-large"})

    password = PasswordField(validators=[
        InputRequired(),
        Length(min=8, max=100)
    ],
        render_kw={"placeholder": "Password", "class": "input is-large"})

    repeat_password = PasswordField(validators=[
        InputRequired(),
        Length(min=8, max=100),
        EqualTo('password', message='Both password fields must be equal!')
    ],
        render_kw={"placeholder": "Repeat Password", "class": "input is-large"})

    submit = SubmitField("Register", render_kw={"class": "button is-block is-info is-large is-fullwidth"})

    def validate_username(self, username):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        digits = '1234567890'
        existing_username = Users.query.filter_by(username=username.data).first()
        beginning_letter = username.data[0].lower() in alphabet
        matching_letters = True
        for symb in username.data:
            if not (symb in alphabet or symb == '_' or symb in digits or symb in alphabet.upper()):
                matching_letters = False
                break
        print(f'DEBUG | existing_username = {existing_username}, beginning_letter = {beginning_letter}')
        print(f'DEBUG | matching_letters = {matching_letters}')
        if existing_username is not None:
            print(f'DEBUG | User exists')
            raise ValidationError('That user already exists.')
        if not (beginning_letter or matching_letters):
            print(f'DEBUG | Invalid username')
            raise ValidationError('Invalid username.')

    def validate_email(self, email):
        existing_email = Users.query.filter_by(email=email.data).first()
        email_matches = '@' in email.data
        print(f'DEBUG | existing_email = {existing_email}, email_matches = {email_matches}')
        if existing_email is not None:
            print(f'DEBUG | Email exists.')
            raise ValidationError('Email already registered.')
        if not email_matches:
            print(f'DEBUG | Invalid email')
            raise ValidationError('Invalid email.')

    def validate_password(self, password):
        password_string = password.data
        symbols = '%$#@&*^|\/~[]{}(),._-'
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        digits = '1234567890'
        contains_symbol = False
        contains_uppercase = False
        contains_lowercase = False
        contains_number = False
        contains_invalid_symbols = True
        for symb in password_string:
            if symb in symbols:
                contains_symbol = True
            elif symb in digits:
                contains_number = True
            elif symb in alphabet:
                contains_lowercase = True
            elif symb in alphabet.upper():
                contains_uppercase = True
            else:
                contains_invalid_symbols = False
        print(f'DEBUG | contains_symbol = {contains_symbol}, contains_uppercase = {contains_uppercase}')
        print(f'DEBUG | contains_lowercase = {contains_lowercase}, contains_number = {contains_number}')
        print(f'DEBUG | contains_invalid_symbols = {contains_invalid_symbols}')
        if contains_symbol and contains_uppercase and contains_lowercase\
                and contains_number and not contains_invalid_symbols:
            print(f'DEBUG | Invalid password')
            raise ValidationError("Invalid password.")


class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(),
        Length(min=6, max=100)
    ],
        render_kw={"placeholder": "Username", "class": "input is-large"})

    password = PasswordField(validators=[
        InputRequired(),
        Length(min=8, max=100)
    ],
        render_kw={"placeholder": "Password", "class": "input is-large"})
    submit = SubmitField('Login', render_kw={"class": "button is-block is-info is-large is-fullwidth"})
