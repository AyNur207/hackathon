from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegForm(FlaskForm):  # форма регистрации
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повтор пароля', validators=[DataRequired()])
    phone_number = StringField('Телефон', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')