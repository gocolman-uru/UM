from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import json
import requests
from flask_wtf.csrf import CSRFProtect
import csv

import pytesseract
from PIL import Image
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score






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




@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save('uploads/' + file.filename)

    # imagen a texto ocr - tesseract
    image = Image.open('uploads/' + file.filename)
    text = pytesseract.image_to_string(image)
    palabras = text.split()
    # cargo el modelo
    loaded_model = joblib.load('modelo_lg.pkl')
    # cargo el vect
    vectorizer = joblib.load('vectorizador.pkl')
    #prediction = loaded_model.predict([text])[0]

    preds_dict = {}

    for palabra in palabras:
        text_vectorized = vectorizer.transform([palabra])
        prediction = loaded_model.predict(text_vectorized)[0]
        preds_dict[palabra] = prediction


    df = pd.read_csv('2_machine_learning/bases/df_predicciones.csv',sep='|')

    libros_lista = []
    for valor in preds_dict.values():
        libros = df.loc[df['Tema'] == valor]['Texto'].values
        libros_lista.append(libros)

    lista_final = []
    for i in libros_lista:
        for u in i:
            lista_final.append(u)

            # test 

    return render_template("recomendaciones.html", uploaded=True, text=text, lista_final=lista_final,palabras=palabras)


