from flask import Flask, jsonify
from flask_mail import Mail
from flasgger import Swagger

import config
from blueprints.avisos_bp import avisos_bp
from blueprints.admin_bp  import admin_bp
from blueprints.auth_bp     import auth_bp
from blueprints.ocean_bp    import ocean_bp
from blueprints.stations_bp import stations_bp
from blueprints.library_bp  import library_bp
from blueprints.contact_bp  import contact_bp
from blueprints.files_bp    import files_bp

SWAGGER_CONFIG = {
    "title": "OOGSJ API",
    "uiversion": 3,
    "version": "1.0.0",
    "description": (
        "API del Observatorio Oceanográfico del Golfo San Jorge. "
        "Expone datos de estaciones meteorológicas, boya oceanográfica, "
        "mareógrafo, biblioteca científica y contacto institucional."
    ),
    "termsOfService": "",
    "contact": {
        "name": "OOGSJ",
        "email": "franco.garcia@conocimiento.gob.ar"
    },
    "license": {"name": ""},
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs",
    "tags": [
        {"name": "Auth",      "description": "Autenticación y sesión"},
        {"name": "Admin",     "description": "Panel de administración (requiere is_admin)"},
        {"name": "Ocean",     "description": "Mareógrafo, boya y predicción de marea"},
        {"name": "Stations",  "description": "Estaciones meteorológicas APPCR"},
        {"name": "Library",   "description": "Biblioteca científica y papers"},
        {"name": "Avisos",    "description": "Avisos al navegante (SHN Argentina)"},
        {"name": "Contact",   "description": "Formulario de contacto y sugerencias"},
        {"name": "Files",     "description": "Archivos y documentos subidos"},
    ],
}


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.update(
        MAIL_SERVER         = config.MAIL_SERVER,
        MAIL_PORT           = config.MAIL_PORT,
        MAIL_USE_TLS        = config.MAIL_USE_TLS,
        MAIL_USERNAME       = config.MAIL_USERNAME,
        MAIL_PASSWORD       = config.MAIL_PASSWORD,
        MAIL_DEFAULT_SENDER = config.MAIL_DEFAULT_SENDER,
        UPLOAD_FOLDER       = config.UPLOAD_FOLDER,
    )
    Mail(app)
    Swagger(app, config=SWAGGER_CONFIG, merge=True)

    app.register_blueprint(auth_bp)
    app.register_blueprint(ocean_bp)
    app.register_blueprint(stations_bp)
    app.register_blueprint(library_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(avisos_bp)
    app.register_blueprint(admin_bp)

    return app


app = create_app()


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)