import os
from flask import Flask
from dotenv import load_dotenv
from api.hazards import hazards_bp
from api.risk_assessment import risk_bp

load_dotenv()
app = Flask(__name__)
app.register_blueprint(hazards_bp, url_prefix='/api')
app.register_blueprint(risk_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
