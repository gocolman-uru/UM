from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import json
import requests
from flask_wtf.csrf import CSRFProtect
import csv





app = Flask(__name__)

csrf = CSRFProtect()


app.secret_key = 'secret_key' 
login_manager = LoginManager()
login_manager.init_app(app)



class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'admin': {'password': 'admin123'}, 'gcolman1': {'password': 'gcolman1'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# Rutas de la aplicación
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and password == users[username]['password']:
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'error')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')




@app.route('/home')
def home():
    return render_template('index.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/search')
def search():

    query = request.args.get('query')
    with open('1_bases_de_datos_ficticias/bases/libros.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        results_final = []
        for row in reader:
            if str(query).lower() in row[0].lower():
                results_nombre = [row[0].split('|')[1]]
                results_link = [row[0].split('|')[7]]
                print([results_nombre+results_link])
                results_final.append([results_nombre+results_link])
    return render_template('search.html', results=results_final)
















