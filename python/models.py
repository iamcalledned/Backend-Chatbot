from extensions import db, bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    system_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class AuthDetails(db.Model):
    __tablename__ = 'auth_details'
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(256))
    system_id = db.Column(db.Integer, db.ForeignKey('user_info.system_id'), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


