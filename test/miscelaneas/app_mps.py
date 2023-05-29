import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, escape
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash




dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir #configuración
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.secret_key = '123'

class Usuario(db.Model):#BBDD Usuarios
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), nullable=False)
	apellido = db.Column(db.String(50), nullable=False)
	documento = db.Column(db.String(10), nullable=False)
	rango_edad1 = db.Column(db.String()) 
	# 1=hasta 18 \ 2=entre 18 y 26 \ 3=entre 27 y 59 \4=mas de 60
	genero = db.Column(db.String())
	#genero masculino, femenino, otro
	password = db.Column(db.String(50), nullable=False)

class Doctor(db.Model):#BBDD Usuarios
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), nullable=False)
	apellido = db.Column(db.String(50), nullable=False)
	documento = db.Column(db.String(10), nullable=False)
	rango_edad1 = db.Column(db.String()) 
	# 1=hasta 18 \ 2=entre 27 y 59 \ 3=entre 18 y 26 \4=mas de 60
	genero = db.Column(db.String())
	#genero masculino, femenino, otro
	password = db.Column(db.String(50), nullable=False)

class Perfil(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	documento = db.Column(db.String(10), nullable=False)
	estudiante = db.Column(db.String())
	deporte = db.Column(db.String())
	viajar = db.Column(db.String())
	lectura = db.Column(db.String())
	rapidez = db.Column(db.String())
	congenio = db.Column(db.String())
	hijos = db.Column(db.String())

class Perfildoc(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	documento = db.Column(db.String(10), nullable=False)
	estudiante = db.Column(db.String())
	deporte = db.Column(db.String())
	viajar = db.Column(db.String())
	lectura = db.Column(db.String())
	rapidez = db.Column(db.String())
	congenio = db.Column(db.String())
	hijos = db.Column(db.String())

class Calif(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	puntualidad = db.Column(db.Integer())
	trato = db.Column(db.Integer())
	detalle = db.Column(db.Integer())
	comunicacion = db.Column(db.Integer())
	recomendacion = db.Column(db.Integer())
	comentario = db.Column(db.String())
	doc = db.Column(db.String())



@app.route('/')
@app.route('/inicio')
def index():
	return render_template('index.html')




@app.route('/signup', methods=['GET', 'POST']) 
def signup():
	if request.method == 'POST':
		cifrado = generate_password_hash(request.form['password'], method="sha256")
		
		if request.form['doctor'] == '1':
			new_doc = Doctor(nombre=request.form['nombre'],
								apellido=request.form['apellido'],
								documento=request.form['documento'],
								rango_edad1=request.form['rango_edad1'],
								genero=request.form['genero'],
								password=cifrado)
			db.session.add(new_doc)
			db.session.commit()
			#guardo info en cookie
			resp = redirect(url_for('perfil'))
			resp.set_cookie('cedula',json.dumps(dict(request.form.items())))
		else:
			new_user = Usuario(nombre=request.form['nombre'],
								apellido=request.form['apellido'],
								documento=request.form['documento'],
								rango_edad1=request.form['rango_edad1'],
								genero=request.form['genero'],
								password=cifrado)
			db.session.add(new_user)
			db.session.commit()
			resp = redirect(url_for('perfil'))
			resp.set_cookie('cedula',json.dumps(dict(request.form.items())))

		return resp
	return render_template('signup.html')




@app.route('/login',methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		login = Usuario.query.filter_by(documento=request.form['documento']).first()#buscamos usuario por DOC, sólo el primero
		
		if login and check_password_hash(login.password, request.form['password']): #comparación de contraseñas
			
			session['documento'] = request.form['documento']
			response = redirect(url_for('Menu'))
			response.set_cookie('cedula',json.dumps(dict(request.form.items())))
			
			return response

		
		login = Doctor.query.filter_by(documento=request.form['documento']).first()	
		
		if login and check_password_hash(login.password, request.form['password']):

			response = redirect(url_for('Menudoc'))
			response.set_cookie('cedula',json.dumps(dict(request.form.items())))
			
			return response
		else:
			return render_template('login.html')


	return render_template('login.html')

@app.route('/logout')
def logout():

	session.pop('documento', None) 
	return render_template('index.html')


#Perfil de usuario
@app.route('/perfil',methods=['GET', 'POST'])
def perfil():
	if request.method == 'POST':
		#primary_key = Usuario.query.filter_by(documento=request.form['documento']).first()
		doc = json.loads(request.cookies.get('cedula'))
		dni = doc.get('documento')
		med = doc.get('doctor')
		if med == '0': #perfil de los usuarios
			user = Usuario.query.filter_by(documento=dni).first()
			data = user.documento

			new_perfil = Perfil(estudiante=request.form['estudiante'],
								deporte=request.form['deporte'],
								viajar=request.form['viajar'],
								lectura=request.form['lectura'],
								rapidez=request.form['rapidez'],
								congenio=request.form['congenio'],
								hijos=request.form['hijos'],
								documento=data)

			db.session.add(new_perfil)
			db.session.commit()
			resp = redirect(url_for('Menu'))
			return resp
		else: #perfil de los doctores
			user = Doctor.query.filter_by(documento=dni).first()
			data = user.documento
			new_perfil = Perfildoc(estudiante=request.form['estudiante'],
								deporte=request.form['deporte'],
								viajar=request.form['viajar'],
								lectura=request.form['lectura'],
								rapidez=request.form['rapidez'],
								congenio=request.form['congenio'],
								hijos=request.form['hijos'],
								documento=data)
			db.session.add(new_perfil)
			db.session.commit()
			resp = redirect(url_for('Menudoc'))
			return resp

	return render_template('perfil.html')



#Calificacion del usuario
@app.route('/calif',methods=['GET', 'POST'])
def calif():
	if request.method == 'POST':
		new_calif=Calif(puntualidad=request.form['puntualidad'],
							trato=request.form['trato'],
							detalle=request.form['detalle'],
							comunicacion=request.form['comunicacion'],
							recomendacion=request.form['recomendacion'],
							comentario=request.form['comentario'],
							doc=request.form['doc'])
		db.session.add(new_calif)
		db.session.commit()
		resp = redirect(url_for('Menu'))
		return resp

	return render_template('calif.html')	



#Pantalla del paciente/usuario
@app.route('/menu',methods=['GET', 'POST'])
def Menu():

	doc = json.loads(request.cookies.get('cedula'))
	dni = doc.get('documento')
	user = Usuario.query.filter_by(documento=dni).first()
	name = user.nombre
	last_name = user.apellido
	data = user.documento

	if 'documento' in session:
		return render_template('menu.html',
							name=name, 
							last_name=last_name, 
							documento=data)
	else:
		return render_template('login.html')



#Pantalla del doctor
@app.route('/menudoc',methods=['GET', 'POST'])	
def Menudoc():

	doc = json.loads(request.cookies.get('cedula'))
	dni = doc.get('documento')
	user = Doctor.query.filter_by(documento=dni).first()
	name = user.nombre
	last_name = user.apellido
	data = user.documento
	promedioc, recomendacion = Mps(data)
	return render_template('menudoc.html',
							name=name, 
							last_name=last_name, 
							documento=data,
							promedio=promedioc,
							recomendacion=recomendacion)

def Mps(data):
	suma = 0
	rec = 0

	doctor = Calif.query.filter_by(doc=data).all()
	
	for c in range(len(doctor)):
		suma = suma + doctor[c].puntualidad
		suma = suma + doctor[c].trato
		suma = suma + doctor[c].detalle
		suma = suma + doctor[c].comunicacion

	for c in range(len(doctor)):
		rec = rec + doctor[c].recomendacion

	try:	
		promedio = suma / (len(doctor) * 4)
		recomendacion = rec / len(doctor) #cantidad de elementos
		promedio = promedio * 100
		recomendacion = recomendacion * 100
	except ZeroDivisionError:
		promedio = 0
		recomendacion = 0
		

	return promedio, recomendacion
		

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

