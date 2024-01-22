from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, DateField, SelectField, IntegerField, FloatField, \
    SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from wtforms.fields import TelField, EmailField

class LoginForm(FlaskForm):
    email_address = EmailField("", validators=[InputRequired(), Email()], render_kw={"placeholder": "Email Address", "class": "form-control"}, default='test@test.com')
    password = PasswordField("", validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Password", "class": "form-control"})
    remember_me = BooleanField('Remember Me')
    login_submit = SubmitField("Login", render_kw={"class": "btn submit", "type": "submit"})


class RegisterForm(FlaskForm):

    email_address = EmailField("Email:", validators=[InputRequired(), Email()], render_kw={"placeholder": "Email Address", "class": "form-control"}, default='test@test.com')
    first_name = StringField("First name:", validators=[InputRequired(), Length(min=1, max=30)], render_kw={"placeholder": "First Name"}, default='')
    last_name = StringField("Last name:", validators=[InputRequired(), Length(min=1, max=30)], render_kw={"placeholder": "Last Name"}, default='')
    phone_number = StringField("Phone No. :", validators=[InputRequired(), Length(min=1, max=15)], render_kw={"placeholder": "Phone Number"}, default='')
    # UserType = SelectField("", validators=[InputRequired()], choices=[(
    #     "customer", "customer"), ("staff", "staff"), ("admin", "admin")])
    address = StringField("Address:", validators=[], render_kw={"placeholder": "Address"})
    date_of_birth = DateField("Date of birth:", validators=[], render_kw={"placeholder": "Date of Birth"})
    password = PasswordField("Password:", validators=[InputRequired(), Length(min=8, max=50)], render_kw={"placeholder": "Password"}, default='password')
    confirm_password = PasswordField("Confirm Password:", validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Confirm Password"}, default='password')
    register_submit = SubmitField("Register", render_kw={"class": "btn submit", "type": "submit"})