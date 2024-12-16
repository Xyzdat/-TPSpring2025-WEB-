from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, DateTimeField

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    user_group = SelectField('Выбере пользователя, за которого вы зайдёте', choices=[('user','Пользователь'),('worker', 'Менеджер, продавец, Диспетчер'), ('courier', 'Курьер')])
    remember_me = BooleanField('Запомнить меня')
    submit  = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username  = StringField('Имя Пользователя', validators=[DataRequired()])
    email = StringField('Введите почту', validators=[DataRequired(), Email()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    password2 = PasswordField('Введите пароль ещё раз', validators=[DataRequired(), EqualTo('password')])
    submit  = SubmitField('Зарегистрироваться')

class OrderForm(FlaskForm):
    date = DateTimeField('Введите дату, к которой было бы удобно доставить цветы.', validators= [DataRequired()])
    adres = StringField('Введите ваш адрес.', validators= [DataRequired()])
    submit  = SubmitField('Оформить заказ')