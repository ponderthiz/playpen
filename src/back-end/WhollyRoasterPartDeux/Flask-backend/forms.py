from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    uname = StringField("Username", [Length(min=3, message="Username must be greater than 3 characters."), DataRequired()])
    pword = PasswordField("Password", [DataRequired()])
    confirm = PasswordField("Confirm Password", [DataRequired(), EqualTo("pword", message="Passwords must match!")])
    submit = SubmitField("Sign In")
