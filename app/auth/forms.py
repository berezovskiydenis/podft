# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField, SubmitField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(
            label='Username',
            validators=[DataRequired()],
            render_kw={'class': 'u-full-width', 'placeholder': 'Username'},
            id='usernameInput'
        )
    password = PasswordField(
            label='Password',
            validators=[DataRequired()],
            render_kw={'class': 'u-full-width', 'placeholder': 'Password'},
            id='passwordInput'
        )
    remember_me = BooleanField("Remember me")
    submit = SubmitField(
            label='Sign In',
            render_kw={'class': 'button-primary'}
        )


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(max=128)],
        render_kw={'class': 'u-full-width', 'placeholder': 'Username'},
        id='usernameInput'
    )
    password = PasswordField(
            label='Password',
            validators=[DataRequired()],
            render_kw={'class': 'u-full-width', 'placeholder': 'Password'},
            id='passwordInput'
        )
    password2 = PasswordField(
        label='Repeat password',
        validators=[EqualTo('password'), DataRequired()],
        render_kw={'class': 'u-full-width', 'placeholder': 'Repeat password'},
        id='passwordInput2'
    )
    submit = SubmitField(
            label='Register',
            render_kw={'class': 'button-primary'}
        )

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already registered.")
