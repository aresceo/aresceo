from app import db
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Utente(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Articolo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(200), nullable=False)
    contenuto = db.Column(db.Text, nullable=False)
    immagine_data = db.Column(db.Text, nullable=True)
    data = db.Column(db.DateTime, default=datetime.datetime.now)
    autore_id = db.Column(db.Integer, db.ForeignKey('utente.id'), nullable=True)
    
    def __init__(self, titolo, contenuto, immagine_data=None, autore_id=None):
        self.titolo = titolo
        self.contenuto = contenuto
        self.immagine_data = immagine_data
        self.autore_id = autore_id
    
    def to_dict(self):
        return {
            "id": self.id,
            "titolo": self.titolo,
            "contenuto": self.contenuto,
            "immagine_data": self.immagine_data,
            "data": self.data.strftime("%Y-%m-%d %H:%M:%S"),
            "autore_id": self.autore_id
        }