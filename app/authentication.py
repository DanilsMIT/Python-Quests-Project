from flask import Blueprint, g,render_template,request,url_for,redirect,flash,session
from werkzeug.security import generate_password_hash, check_password_hash
#tabla user
from .dataBase import User
#data base
from app import db



bp = Blueprint('authentication',__name__, url_prefix='/authentication')


@bp.route('/login',methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        user_name = request.form['login-user']
        user_password = request.form['login-password']
        #Validar usuario
        userLogin = User.query.filter_by(username = user_name).first()
        error = None
        if userLogin == None :
            error = 'Usuario o Contraseña Incorrectos'
        elif not check_password_hash(userLogin.userpassword,user_password):
            error = 'Usuario o Contraseña Incorrectos'

        #Login/ Iniciar session
        if error is None:
            session.clear()
            session['user_id'] = userLogin.id
            return redirect(url_for('Quests.list'))
        flash(error)
    return render_template('authentication/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        user_name = request.form['register-user']
        user_password = request.form['register-password']
        usuario = User(user_name,generate_password_hash(user_password))

        #COMPROBAR / AGREGAR USUARIO
        usuario_obtenido = User.query.filter_by(username = user_name).first()
        if usuario_obtenido is None:
            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('authentication.login'))
        else:
            flash("usuario ya registrado")

    return render_template('authentication/register.html')
    
@bp.before_app_request
def logged_user():
    userID =  session.get('user_id')
    if userID is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(userID)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

import functools
def login_required(view):
    @functools.wraps(view)
    def wrapped_view( ** kwargs):
        if g.user is None:
            return redirect(url_for('authentication.login'))
        return view( ** kwargs)
    return wrapped_view