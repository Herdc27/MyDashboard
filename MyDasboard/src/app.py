import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

import models.models
from ext import db, jwt, ma, migrate
from resources import bp as api_bp
from routes.auth_route import auth_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    usuario = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    servidor = os.getenv("DB_HOST")
    puerto = os.getenv("DB_PORT")
    base_datos = os.getenv("DB_NAME")

    # Ajustes de usuario/contra/host segun el entorno
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{usuario}:{password}@{servidor}:{puerto}/{base_datos}"
    )
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    # CORS
    CORS(
        app,
        resources={
            r"/mydashboard/*": {
                "origins": ["http://localhost:5173"],  # react vite
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
            },
            r"/*": {
                "origins": ["http://localhost:5173"],  # react vite
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type"],
                "supports_credentials": True,
            },
        },
    )

    # Blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)

    @app.route("/mydashboard")
    def home():
        return "Api de .."

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
