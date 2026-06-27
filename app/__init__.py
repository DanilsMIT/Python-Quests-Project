from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def create_app():
    app = Flask(__name__)
    #configuración
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'key',
        SQLALCHEMY_DATABASE_URI = "sqlite:///quests.db"
    )
    db.init_app(app)

    #bluePrints
    from . import Quests
    app.register_blueprint(Quests.bp)

    from . import authentication
    app.register_blueprint(authentication.bp)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    #Migrar tablas a la base de datos
    with app.app_context():
        db.create_all()
    
    return app

