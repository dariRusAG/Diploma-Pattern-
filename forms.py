from wtforms import Form, StringField, PasswordField, validators, widgets


class AuthorizationForm(Form):
    auth_login = StringField("Логин", [validators.InputRequired()])
    auth_password = PasswordField("Пароль", [validators.InputRequired()])


class RegistrationForm(Form):
    reg_login = StringField("Логин", [validators.InputRequired(), validators.Length(min=4, max=25)])
    reg_password = PasswordField('Пароль', [
        validators.InputRequired(),
        validators.Length(min=8, max=60),
        validators.EqualTo('password_confirm', message='Пароли должны совпадать')
    ])
    password_confirm = PasswordField('Повторите пароль')
