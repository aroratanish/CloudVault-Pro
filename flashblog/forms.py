from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,SelectField
from wtforms.validators import ValidationError,DataRequired,Length,Email,equal_to
from flashblog.models import User
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),equal_to('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username already taken please choose different')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already taken please choose different')
        
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember  = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('username already taken please choose different')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('email already taken please choose different')
            
class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit= SubmitField('Post') 

class RequestResetForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        user = User.query.filter_by(
            email=email.data
        ).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. '
                'You must register first.'
            )
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),equal_to('password')])
    submit = SubmitField('Reset Password')

class UploadFileForm(FlaskForm):
    folder = SelectField(
        'Folder',
        coerce=int
    )
    file = FileField(
        'Upload File',
        validators=[
            FileAllowed(
                ['pdf','txt','jpg','jpeg','png','docx'],
                'Only valid files allowed'
            )
        ]
    )
    submit = SubmitField('Upload')

class FolderForm(FlaskForm):
    name = StringField(
        'Folder Name',
        validators=[DataRequired(),Length(min=2,max=50)]
    )
    submit = SubmitField(
        'Create Folder'
    )