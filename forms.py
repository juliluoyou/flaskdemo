from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username=StringField(label='user_', validators=[DataRequired()])
    password=PasswordField(label='pwd_', validators=[DataRequired()])
    submit=SubmitField(label='submit_')