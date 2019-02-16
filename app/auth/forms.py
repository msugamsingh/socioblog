from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(FlaskForm):

    email_or_username = StringField('Email or Username', validators=[
                        DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):

    email = StringField('Email', validators=[
                        DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp(
        '^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only numbers, letters, dots or underscore.')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'password2', message='Password did not match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(FlaskForm):

    old_password = PasswordField("Old Password", validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm New Password',
                              validators=[DataRequired()])
    submit = SubmitField("Update Password")


class PasswordResetRequestForm(FlaskForm):

    email = StringField('Email', validators=[
                        DataRequired(), Length(1, 64), Email()])
    submit = SubmitField("Reset Password")


class PasswordResetForm(FlaskForm):

    password = PasswordField("New Password", validators=[
                             DataRequired(), EqualTo('password2', message="Password must match")])
    password2 = PasswordField("Confirm New Password",
                              validators=[DataRequired()])
    submit = SubmitField("Reset Password")


class ChangeEmailForm(FlaskForm):

    email = StringField("New Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Update Email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.date).first():
            raise ValidationError('Email already registered.')
