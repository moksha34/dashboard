from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,validators,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class Signupform(FlaskForm):

    username = StringField("username",validators=[DataRequired(),Length(min=2,max=20,message="username between 2 to 20 chars")])
    email =  StringField("email",validators=[DataRequired(),Email(message="enter a valid email")])
    password = PasswordField("password",validators=[DataRequired()])
    confirm_password=PasswordField("confirm password",validators=[DataRequired(),EqualTo("password")])
    submitbutton = SubmitField("Sign up!")

class Loginform(FlaskForm):
    email =  StringField("email",validators=[DataRequired(),Email(message="enter a valid email")])
    password = PasswordField("password",validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submitbutton = SubmitField("Login")