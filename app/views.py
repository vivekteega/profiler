from app import app
import pandas as pd 
from flask import request, render_template, flash, redirect
from sqlalchemy import create_engine
import json
from .forms import SQLINTF, replaceNull, fuzzyDedup, findDuplicate, loginForm, kmeanForm, recipeForm, Program

#GET REQUEST

@app.route('/')
def welcome():
	engine = create_engine(dbURI)
	connection = engine.connect()
	connection.close()
	engine.dispose()
	return render_template('base.html',tablenames=tablenames)

@app.route('/reference')
def welcome1():
	engine = create_engine(dbURI)
	connection = engine.connect()
	frame = pd.read_sql('show tables',connection)
	connection.close()
	engine.dispose()
	return render_template('dashboard.html',tablenames=tablenames)

@app.route('/test',methods=['GET','POST'])
def welcome2():
	#form = recipeForm(request.form)
	#categories = [['vivek',"Vivek"],['vamsi',"Vamsi"],['gary',"Gary"],['sharvik',"Sharvik"]]
	#form = recipeForm(request.form)
	#form.category.choices = categories
	form = Program()
	return render_template('temporary.html', form=form)

@app.route('/dataquality',methods=['GET','POST'])
def dataQuality(): 
	engine = create_engine(dbURI)
	connection = engine.connect()
	frame = pd.read_sql('show tables',connection)
	tableform = []
	for cur in tablenames:
		tableform.append([cur,cur])

	sqlform = SQLINTF()
	if sqlform.validate_on_submit():
		result = connection.execute(str(sqlform.query.data))
		connection.close()
		engine.dispose()
		flash('Query executed')
		return redirect('/dataquality')

	finddupform = findDuplicate(request.form)
	finddupform.tablen.choices = tableform
	if finddupform.validate_on_submit():
		#do something 
		return redirect('/dataquality')

	repnullform = replaceNull(request.form)
	repnullform.tablen.choices = tableform
	if repnullform.validate_on_submit():
		queryString = "update " + str(repnullform.tablen.data) + " set " + str(repnullform.columnn.data) + " = '"+str(repnullform.repvalue.data)+"' where "+ str(repnullform.columnn.data) +" is null;"
		result = connection.execute(queryString) 
		connection.close()
		engine.dispose()
		flash('Query executed')
		return redirect('/dataquality')

	fuzzydedupform = fuzzyDedup()
	fuzzydedupform.tablen.choices = tableform
	if fuzzydedupform.validate_on_submit():
		#queryString = "update " + str(fuzzydedupform.tablen.data) + " set " + str(fuzzydedupform.columnn.data) 
		#result = connection.execute(queryString) 
		connection.close()
		engine.dispose()
		flash('Query executed')
		return redirect('/dataquality')

	kmeanform = kmeanForm()
	if kmeanform.validate_on_submit():
		#queryString = "update " + str(fuzzydedupform.tablen.data) + " set " + str(fuzzydedupform.columnn.data) 
		#result = connection.execute(queryString) 
		connection.close()
		engine.dispose()
		flash('Query executed')
		return redirect('/dataquality')


	connection.close()
	engine.dispose()
	return render_template('modal.html',tablenames=tablenames, sqlform=sqlform, repnullform = repnullform, dedupform = fuzzydedupform, kmeanform=kmeanform, finddupform = finddupform)


@app.route('/metadata',methods=['GET','POST'])
def metadata(): 
	engine = create_engine(dbURI)
	connection = engine.connect()

	option = request.args.get('card')

	if option == 'generalinfo':
		return render_template('meta-geninfo.html', dbURI=dbURI, curtable = 'General Info')

	if option == 'limitinfo':
		return render_template('meta-liminfo.html', dbURI=dbURI, curtable = 'Limitation Info')

	if option == 'functioninfo':
		return render_template('meta-funcinfo.html', dbURI=dbURI, curtable = 'Function Info')

	if option == 'cataloginfo':
		frame = pd.read_sql('show tables', connection)
		frame_html = frame.to_html()
		frame_html =frame_html.replace('<table border="1" class="dataframe">', '<table id="example" class="table table-striped table-bordered" cellspacing="0" width="60%" >')
		return render_template('meta-catinfo.html', tables = frame_html, dbURI=dbURI, curtable = 'Catalog Info')

	if option == 'indexinfo':
		templst = []
		for cur in tablenames:
			que = "show index from " + str(cur)
			tframe = pd.read_sql(que, connection)
			templst.append(tframe)
		frame = pd.concat(templst)
		frame = frame.reset_index(drop=True)
		frame_html = frame.to_html()
		frame_html =frame_html.replace('<table border="1" class="dataframe">', '<table id="example" class="table table-striped table-bordered" cellspacing="0" width="60%" >')
		return render_template('meta-indexinfo.html', tables = frame_html, dbURI=dbURI, curtable = 'Function Info')


	connection.close()
	engine.dispose()
	return render_template('metadata.html',tablenames=tablenames)

@app.route('/tools',methods=['GET','POST'])
def tools(): 
	engine = create_engine(dbURI)
	connection = engine.connect()
	frame = pd.read_sql('show tables',connection)

	sqlform = SQLINTF()
	if sqlform.validate_on_submit():
		result = connection.execute(str(sqlform.query.data))
		connection.close()
		engine.dispose()
		flash('Query executed')
		return redirect('/tools')


	connection.close()
	engine.dispose()
	return render_template('tools.html',tablenames=tablenames, sqlform=sqlform)

@app.route('/login',methods=['GET','POST'])
def login(): 
	loginform = loginForm()
	if loginform.validate_on_submit():
		global dbURI
		dbURI = "mysql://"+str(loginform.dbusername.data)+":"+str(loginform.dbpassword.data)+"@"+str(loginform.dbname.data)
		engine = create_engine(dbURI)
		connection = engine.connect()
		
		global tablenames 
		tablenames = pd.read_sql('show tables',connection)
		tempstring = "Tables_in_" + str(loginform.dbname.data.split("/",1)[1])
		tablenames = tablenames[tempstring].tolist()

		global columndict 
		columndict = {}
		for cur in tablenames: 
			temp = pd.read_sql('show columns in '+str(cur)+";", connection)
			temp = temp["Field"].tolist()
			columndict[cur] = temp
		connection.close()
		engine.dispose()
		#flash('Query executed')
		return redirect('/')
		#return str(columndict)

	return render_template('login-page.html', loginform=loginform)

# 1. Fetch table from the specified database
@app.route('/table')
def getTable():
	engine = create_engine("mysql://root:hello@localhost/employees")
	connection = engine.connect()
	tablename = request.args.get('name')
	frame = pd.read_sql("select * from " + str(tablename),connection).head(100)
	connection.close()
	engine.dispose()
	frame_html = frame.to_html()
	frame_html =frame_html.replace('<table border="1" class="dataframe">', '<table id="example" class="table table-striped table-bordered" cellspacing="0" width="60%" >')
	#frame_html = frame_html.replace('</th>', '<a href="' + 'localhost:5000'+'" class="button">c</a>' + '</th>' )
	return render_template('table.html',tables = frame_html,curtable=tablename.title(), tablenames=tablenames)


# 2. Fetch column from the specified table
@app.route('/showdata/<tablename>/<colname>')
def getColumn(tablename,colname):
	engine = create_engine(dbURI)
	connection = engine.connect()
	frame = pd.read_sql("select " + str(colname) + " from " + str(tablename),connection)
	connection.close()
	print "This is the name of the column" 
	engine.dispose()
	total = len(frame)
	unique = len(frame[colname].unique())
	null = frame[colname].isnull().sum()
	return render_template('column.html', pltdata = [total, unique, null])
	# data=[total,unique,null])

# 3. Returns frequency statistics of the given column 
@app.route('/report/frequency_statistics/<tablename>/<colname>')
def getFreqstat(tablename, colname):
	engine = create_engine(request.headers.get('dbURI'))
	connection = engine.connect()
	frame = pd.read_sql("select " + str(colname) + " from " + str(tablename),connection)
	connection.close()
	engine.dispose()
	result = frame[colname].value_counts()
	return result.to_json()

# 5. Returns profile information of the given column 
@app.route('/report/profile_info/<tablename>/<colname>')
def getProfilecol(tablename, colname):
	engine = create_engine(request.headers.get('dbURI'))
	connection = engine.connect()
	frame = pd.read_sql("select " + str(colname) + " from " + str(tablename),connection)
	connection.close()
	engine.dispose()
	lst = {'columnName' : colname,
		   'tableName' : tablename,
		   'null ' : frame[colname].isnull().sum(),
		   'unique' : len(frame[colname].unique()),
		   'total' : len(frame[colname]) }
	return json.dumps(lst)

# 5. String lenth analysis 
@app.route('/report/string_len_analysis/<tablename>/<colname>')
def lengthAnalysis(tablename, colname):
	engine = create_engine(request.headers.get('dbURI'))
	connection = engine.connect()
	frame = pd.read_sql("select " + str(colname) + " from " + str(tablename),connection)
	connection.close()
	engine.dispose()
	temp = frame[colname].apply(len)
	lst = {'max' : temp.max(),
	       'min' : temp.min()}
	return json.dumps(lst)

# 6. Returns a list of all the tables in a database
@app.route('/tablelist')
def getTableList():
	engine = create_engine(request.headers.get('dbURI'))
	connection = engine.connect()
	frame = pd.read_sql("show tables",connection)
	connection.close()
	engine.dispose()
	return frame.to_json()

# 7. SQL interface
'''@app.route('/sqlinterface', methods=['GET', 'POST'])
def sqlInterface():	
	form = SQLINTF()
	engine = create_engine(dbURI)
	connection = engine.connect()
	frame = pd.read_sql('show tables',connection)
	
	if form.validate_on_submit():
		engine = create_engine(dbURI)
		connection = engine.connect()
		result = connection.execute(str(form.query.data))
		connection.close()
		engine.dispose()
		flash('Query executed')
		return redirect('/test')
	connection.close()
	engine.dispose()
	return render_template('modal.html',tablenames=frame["Tables_in_employees"].tolist(), form=form)'''

# 8. Replace null
@app.route('/dataquality/replacenull/<tablename>/<colname>')
def repNull(tablename, colname):
	engine = create_engine(dbURI)
	connection = engine.connect()
	replaceValue = request.args.get('value')
	queryString = "update " + str(tablename) + " set " + str(colname) + " = "+str(replaceValue)+" where "+ str(colname) +" is null;"
	connection.execute(queryString)
	return render_template('index.html',tablenames=tablenames)