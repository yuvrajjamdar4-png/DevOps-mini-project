
from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    from app.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/")
    def home():
        return jsonify({
            "project": "Enterprise Student Record & Academic Management Platform",
            "status": "running",
            "health_endpoint": "/api/health",
            "api_endpoints": [
                "/api/students/S001",
                "/api/health",
            ],
        })

    return app
