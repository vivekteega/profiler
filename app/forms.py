from flask_wtf import Form
from wtforms import StringField, BooleanField, SelectField, PasswordField, IntegerField, FormField
from wtforms.validators import DataRequired, Required



class SQLINTF(Form):
    query = StringField('query',  validators=[DataRequired()])

class findDuplicate(Form):
	tablen = SelectField('tablen', validators=[DataRequired()])
	columnn = StringField('columnn', validators=[DataRequired()])

class replaceNull(Form):
	tablen = SelectField('tablen', validators=[DataRequired()])
	columnn = StringField('columnn', validators=[DataRequired()])
	repvalue = StringField('repvalue', validators=[DataRequired()])

class fuzzyDedup(Form):
	tablen = SelectField('tablen', validators=[DataRequired()])
	columnn = StringField('columnn', validators=[DataRequired()])

class kmeanForm(Form):
	tablen = StringField('tablen', validators=[DataRequired()])
	columnn = StringField('columnn', validators=[DataRequired()])	

class loginForm(Form):
	#connname = StringField('tablen', validators=[DataRequired()])
	#dbtype = StringField('columnn', validators=[DataRequired()])
	dbname = StringField('columnn', validators=[DataRequired()])
	dbusername = StringField('columnn', validators=[DataRequired()])
	dbpassword = PasswordField('columnn', validators=[DataRequired()])

class recipeForm(Form):
	category = SelectField('category', choices=[])
	
class Calculator(Form):
	amount = IntegerField('Amount', validators = DataRequired() )
	weight = IntegerField('Amount', validators = DataRequired() )

class Program(Form):
	cycles = IntegerField('Cycles', validators = DataRequired())
	volume = FormField(Calculator)