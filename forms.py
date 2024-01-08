from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField
from wtforms.validators import Email, InputRequired, Length
from flask_wtf.file import FileField


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    image_url = StringField("Image URL (Optional) ")
    header_image_url = StringField("Header Image URL (Optional) ")
    bio = StringField("Bio (Optional) ")
    location = StringField("Location (Optional) ")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])


class PostForm(FlaskForm):
    text = TextAreaField("Text", validators=[InputRequired(), Length(max=148, min=1)])


class UploadForm(FlaskForm):
    image = FileField("Image File")


class EditUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    image_url = StringField("(Optional) Image URL")
    header_image_url = StringField("(Optional) Header Image URL")
    bio = StringField("(Optional) Bio", validators=[Length(max=100)])
    location = StringField("(Optional) Location")


class CommentForm(FlaskForm):
    text = TextAreaField("Text", validators=[InputRequired(), Length(max=148, min=1)])


class MessageForm(FlaskForm):
    text = StringField("Text", validators=[InputRequired(), Length(max=148, min=1)])
