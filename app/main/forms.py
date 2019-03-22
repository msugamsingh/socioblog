from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, SelectField
from wtforms.validators import Required, DataRequired, Length, Email, Regexp
from flask_pagedown.fields import PageDownField
from ..models import Role, User
from ..decorators import admin_required


class EditProfileForm(FlaskForm):

    profile = FileField('Change Photo', validators=[FileAllowed(['jpg', 'png'])]) 
    name = StringField('Name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField("About Me")
    submit = SubmitField("Submit")


class EditProfileAdminForm(FlaskForm):

    email = StringField("Emial", validators=[DataRequired(), Length(1,64), Email()])
    username = StringField("Username", validators=[
        DataRequired(),
        Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9._]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')
    ])
    confirmed = BooleanField('Confirmed')
    role = SelectField("Role", coerce=int)
    name = StringField('Name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField("About Me")
    submit = SubmitField("Submit")

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user
    
    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidatonError("Username alredy in use.")        


class PostForm(FlaskForm):
    
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField("Post")


class CommentForm(FlaskForm):

    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('Comment')