# app.py
from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:Kiki6969!@localhost/credentials'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)
CORS(app)

# Now that db is initialized, we can import User
from models import UserInfo, AuthDetails

# Import routes after models to avoid circular import
from routes import api

app.register_blueprint(api, url_prefix='/api')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



