from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

# Import routes
from routes.categorise import categorise_bp
from routes.query import query_bp
from routes.health import health_bp
from routes.report import report_bp
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.stream import stream_bp
from routes.analyse import analyse_bp
from routes.batch import batch_bp
from routes.webhook import webhook_bp


app = Flask(__name__)
CORS(app)

# ✅ Swagger FIX
app.config['SWAGGER'] = {
    'uiversion': 3
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",  # 🔥 FIXED
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Health AI API",
        "description": "Health Analysis Dashboard",
        "version": "1.0"
    }
}

Swagger(app, config=swagger_config, template=swagger_template)

# Register Blueprints
app.register_blueprint(analyse_bp)
app.register_blueprint(categorise_bp)
app.register_blueprint(query_bp)
app.register_blueprint(health_bp)
app.register_blueprint(report_bp)
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(stream_bp)
app.register_blueprint(batch_bp)
app.register_blueprint(webhook_bp)

@app.route("/")
def home():
    return {"message": "Health API Running 🚀"}

if __name__ == "__main__":
    print("🔥 Server running: http://127.0.0.1:5000")
    print("📄 Swagger: http://127.0.0.1:5000/docs/")
    app.run(debug=True)