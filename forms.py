from wtforms import StringField, BooleanField, Form, PasswordField,validators
from passlib.hash import pbkdf2_sha256
from model import User

class RegistrationForm(Form):
    email = StringField('email', [validators.Length(min=6, max=35,message="Email length must be between 6 to 35 characters."),
                                  validators.DataRequired(),
                                  validators.Email()])
    password = PasswordField('password', [validators.DataRequired(),
       validators.Length(min=6, max=35, message="Password length must be between 6 to 35 characters."),
       validators.Regexp('^(?=.*[a-zA-Z])(?=.*[0-9])',message='Password must contain at least one letter and one number.'),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('confirm')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            self.email.errors.append('Email in use.')
            return False

        self.user = user
        return True

class LoginForm(Form):
    email = StringField('email', [validators.Length(min=6, max=35,message="Email length must be between 6 to 35 characters."),
                                  validators.DataRequired(),
                                  validators.Email()])
    password = PasswordField('password', [validators.DataRequired()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.get(self.email.data)
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not pbkdf2_sha256.verify(self.password.data, user.password):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True
