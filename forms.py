from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, DateField, SelectField, IntegerField, FloatField, \
    SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from wtforms.fields import TelField, EmailField

class LoginForm(FlaskForm):
    emailField = EmailField("", validators=[InputRequired(), Email()], render_kw={
        "placeholder": "Email Address"})
    password = PasswordField("", validators=[InputRequired(), Length(
        min=1, max=50)], render_kw={"placeholder": "Password"})
    RegisterSubmit = SubmitField("Login")
    pass

class RegisterForm(FlaskForm):
    FullName = StringField("", validators=[InputRequired(), Length(
        min=1, max=30)], render_kw={"placeholder": "Full Name"})
    PhoneNumber = StringField("", validators=[InputRequired(), Length(
        min=1, max=15)], render_kw={"placeholder": "Phone Number"})
    UserType = SelectField("", validators=[InputRequired()], choices=[(
        "customer", "customer"), ("staff", "staff"), ("admin", "admin")])
    Address = StringField("", validators=[], render_kw={
        "placeholder": "Address"})
    EmailAddress = EmailField("", validators=[InputRequired(), Email()], render_kw={
        "placeholder": "Email Address"})
    Password = PasswordField("", validators=[InputRequired(), Length(
        min=1, max=50)], render_kw={"placeholder": "Password"})
    RegisterSubmit = SubmitField("Register")