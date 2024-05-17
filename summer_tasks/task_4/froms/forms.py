from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, SearchField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError
from wtforms.widgets import TextArea


def validate_email_domain(form, field):
    allowed_domains = ['gmail.com']  # список допустимых доменов
    email = field.data
    if email.split('@')[-1] not in allowed_domains:
        raise ValidationError('Допустимый домен: gmail.com')


class BaseUserForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(),
                                             Length(min=5, max=20,
                                                    message="минимальная длина 5 а максимальная 20"),
                                             Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                    message="Только буквы, _, цифры")])
    first_name = StringField('Имя', validators=[DataRequired(),
                                                Length(min=4, max=30,
                                                       message="минимальная длина 4 а максимальная 30"),
                                                Regexp(regex="^[А-Яа-я]+$",
                                                       message="Только буквы")])
    second_name = StringField("Фамилия", validators=[DataRequired(),
                                                     Length(min=4, max=30,
                                                            message="минимальная длина 4 а максимальная 30"),
                                                     Regexp(regex="^[А-Яа-я]+$",
                                                            message="Только буквы")])
    surname = StringField("Отчество", validators=[DataRequired(),
                                                  Length(min=4, max=30,
                                                         message="минимальная длина 4 а максимальная 30"),
                                                  Regexp(regex="^[А-Яа-я]+$",
                                                         message="Только буквы")])
    phone_number = StringField("Номер телефона", validators=[DataRequired(),
                                                              Regexp(regex="^\+7\d{10}$",
                                                                     message="+7 обязательно и длинна составляет 10 цифр")])
    email_name = StringField("Почта", validators=[DataRequired(),
                                                Email(message="Укажите почту с @", ),
                                             Length(min=6, max=30,
                                                     message="минимальное кол-во символов 5 а максимальное 20"),
                                                  validate_email_domain])


class LoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class SearchForm(FlaskForm):
    search = SearchField("Поиск пользователей")
    submit = SubmitField("Искать")


class RegistrationForm(BaseUserForm):
    password = PasswordField("Пароль", validators=[DataRequired(),
                                                   Length(min=8,
                                                          message="Пароль должен содержать как минимум 8 символов"),
                                                   Regexp(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$',
                                                          message="пароль должен содержать как минимум одну заглавную "
                                                                  "букву, одну строчную, одну цифру, один "
                                                                  "специальный символ."),
                                                   EqualTo("confirm",
                                                           message="Пароль не совпадает")])
    confirm = PasswordField("Повторить пароль", validators=[DataRequired(),
                                                              EqualTo("password",
                                                                      message="Пароль не совпадает")])
    submit = SubmitField("Зарегистрироваться")


class EditProfileForm(BaseUserForm):
    submit = SubmitField("Изменить")


class AddUserForm(RegistrationForm):
    submit = SubmitField("Добавить")


class SendMessageForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(),
                                                       Length(min=5,
                                                              max=500,
                                                              message="Максимально символов в заголовке 500 а мимимум 5")])
    message = StringField("Сообщение", validators=[DataRequired(),
                                                   Length(min=2,
                                                          message="минимально символов должно быть больше 2")],
                                                          widget=TextArea())
    submit = SubmitField("Отправить")