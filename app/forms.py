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
	column1 = StringField('column1', validators=[DataRequired()])	
	column2 = StringField('column2', validators=[DataRequired()])

class linearRegression(Form):
	tablen = StringField('tablen', validators=[DataRequired()])
	column1 = StringField('column1', validators=[DataRequired()])	
	column2 = StringField('column2', validators=[DataRequired()])

class loginForm(Form):
	#connname = StringField('tablen', validators=[DataRequired()])
	#dbtype = StringField('columnn', validators=[DataRequired()])
	dbname = StringField('columnn', validators=[DataRequired()])
	dbusername = StringField('columnn', validators=[DataRequired()])
	dbpassword = PasswordField('columnn', validators=[DataRequired()])

class createTable(Form):
	tablename = StringField('tablename', validators=[DataRequired()])
	columnn = StringField('columnn', validators=[DataRequired()])
	datatype = SelectField('datatype', validators=[DataRequired()], choices=[(1, 'BIT'), (2, 'BOOL'), (3, 'TINY INT'), (4, 'TINY UNSIGNED'), (5, 'BIG INT'), (6, 'BIGINT UNSIGNED'), (7, 'LONG VARBINARY'), (8, 'MEDIUMBLOB'), (9, 'LONGBLOB'), (10, 'BLOB'), (11, 'TINYBLOB'), (12, 'VARBINARY'), (13, 'BINARY'), (14, 'LONG VARCHAR'), (15, 'MEDIUMTEXT'), (16, 'LONGTEXT'), (17, 'TEXT'), (18, 'TINYTEXT'), (19, 'CHAR'), (20, 'NUMERIC'), (21, 'DECIMAL'), (22, 'INTEGER'), (23, 'INTEGER UNSIGNED'), (24, 'INT'), (25, 'FLOAT'), (26, 'DOUBLE'), (27, 'REAL'), (28, 'VARCHAR'), (29, 'ENUM'), (30, 'SET'), (31, 'DATE'), (32, 'TIME'), (33, 'DATETIME'), (34, 'TIMESTAMP')])
	notnull = BooleanField('notnull', default=False)
	pkey = BooleanField('pkey', default=False)

class recipeForm(Form):
	category = SelectField('category', choices=[])
	
class Calculator(Form):
	amount = IntegerField('Amount', validators = DataRequired() )
	weight = IntegerField('Amount', validators = DataRequired() )

class Program(Form):
	cycles = IntegerField('Cycles', validators = DataRequired())
	volume = FormField(Calculator)