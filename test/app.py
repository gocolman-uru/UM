from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import json
import requests
from flask_wtf.csrf import CSRFProtect






app = Flask(__name__)

csrf = CSRFProtect()


app.secret_key = 'secret_key' 
login_manager = LoginManager()
login_manager.init_app(app)



# Directorio de la base de datos
#dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"



# Configuración de la base de datos de usuarios (puede ser cualquier base de datos compatible con Flask)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'admin': {'password': 'admin123'}, 'user': {'password': 'user123'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


### Genero las clases necesarias que necesito



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
    # tomo el valor de la busqueda
    query = request.args.get('query')
    return render_template('search.html')




















@app.route('/search_results')
def search_results():
    query = request.args.get('query')
    # Aquí iría tu código para buscar libros en tu base de datos o en la web
    return render_template('search_results.html', books=books)








'''@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and password == users[username]['password']:
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Nombre de usuario o contraseña incorrectos')
    else:
        return render_template('login.html')'''
'''
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
'''
if __name__ == '__main__':
    csrf.init_app(app)
    app.run(debug=True)