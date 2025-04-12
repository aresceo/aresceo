import os
import logging
import datetime
import uuid

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db.init_app(app)

# Configurazione Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Accedi per visualizzare questa pagina'
login_manager.login_message_category = 'warning'

# Import models after initializing db
from models import Articolo, Utente

@login_manager.user_loader
def load_user(user_id):
    return Utente.query.get(int(user_id))

with app.app_context():
    db.create_all()
    
    # Aggiungi un articolo di benvenuto se non ci sono articoli
    articolo_count = Articolo.query.count()
    if articolo_count == 0:
        articolo_benvenuto = Articolo(
            "Benvenuto nel Portale Notizie",
            "Questo è un semplice portale notizie dove puoi leggere e pubblicare articoli. Usa la barra di navigazione per esplorare il sito."
        )
        db.session.add(articolo_benvenuto)
        db.session.commit()
    
    # Crea utente amministratore se non esiste
    admin = Utente.query.filter_by(username="admin").first()
    if not admin:
        admin = Utente(
            username="admin",
            email="admin@example.com",
            password="adminpassword",
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()


@app.route('/')
def home():
    articoli = Articolo.query.order_by(Articolo.data.desc()).all()
    return render_template('home.html', articoli=articoli)


@app.route('/ricerca')
def pagina_ricerca():
    return render_template('search.html')


@app.route('/api/ricerca')
def ricerca_articoli():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    articoli = Articolo.query.filter(
        (Articolo.titolo.ilike(f'%{query}%')) | 
        (Articolo.contenuto.ilike(f'%{query}%'))
    ).all()
    
    return jsonify([articolo.to_dict() for articolo in articoli])


@app.route('/aggiungi', methods=['GET', 'POST'])
@login_required
def aggiungi_articolo():
    # Verifica se l'utente è amministratore
    if not current_user.is_admin:
        flash('Solo gli amministratori possono pubblicare articoli', 'danger')
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        titolo = request.form.get('titolo')
        contenuto = request.form.get('contenuto')
        immagine_data = request.form.get('immagine_data')
        
        if not titolo or not contenuto:
            flash('Titolo e contenuto sono obbligatori!', 'danger')
            return redirect(url_for('aggiungi_articolo'))
        
        nuovo_articolo = Articolo(
            titolo=titolo, 
            contenuto=contenuto, 
            immagine_data=immagine_data,
            autore_id=current_user.id
        )
        
        db.session.add(nuovo_articolo)
        db.session.commit()
        
        flash('Articolo pubblicato con successo!', 'success')
        return redirect(url_for('home'))
    
    return render_template('add_article.html')


@app.route('/articolo/<int:articolo_id>')
def visualizza_articolo(articolo_id):
    articolo = Articolo.query.get_or_404(articolo_id)
    return render_template('article.html', articolo=articolo)


@app.route('/articolo/<int:articolo_id>/elimina', methods=['POST'])
@login_required
def elimina_articolo(articolo_id):
    if not current_user.is_admin:
        flash('Solo gli amministratori possono eliminare articoli', 'danger')
        return redirect(url_for('home'))
        
    articolo = Articolo.query.get_or_404(articolo_id)
    db.session.delete(articolo)
    db.session.commit()
    
    flash('Articolo eliminato con successo', 'success')
    return redirect(url_for('home'))


# Rotte per autenticazione
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username e password sono richiesti', 'danger')
            return redirect(url_for('login'))
            
        utente = Utente.query.filter_by(username=username).first()
        
        if not utente or not utente.check_password(password):
            flash('Username o password non validi', 'danger')
            return redirect(url_for('login'))
            
        login_user(utente)
        flash(f'Benvenuto, {utente.username}!', 'success')
        
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('home'))
        
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Hai effettuato il logout', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
