import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

REGISTRATION_CODE = 'FAHR123'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='student')
    deletion_requested_at = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theory = db.Column(db.Integer, nullable=False)
    driving = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def check_pending_deletion():
    if current_user.is_authenticated and current_user.deletion_requested_at:
        if datetime.utcnow() - current_user.deletion_requested_at > timedelta(hours=24):
            # delete user and related data
            Image.query.filter_by(user_id=current_user.id).delete()
            Rating.query.filter_by(user_id=current_user.id).delete()
            uid = current_user.id
            logout_user()
            User.query.filter_by(id=uid).delete()
            db.session.commit()
            flash('Dein Konto wurde gelöscht.', 'info')
            return redirect(url_for('index'))

@app.route('/')
def index():
    images = Image.query.filter_by(approved=True).all()
    return render_template('index.html', images=images)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        code = request.form.get('code')
        if code != REGISTRATION_CODE:
            flash('Ungültiger Registrierungscode', 'danger')
            return redirect(url_for('register'))
        username = request.form.get('username')
        password = request.form.get('password')
        accept = request.form.get('accept')
        if not accept:
            flash('Du musst die Datenschutzbestimmungen akzeptieren.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Benutzername bereits vergeben.', 'danger')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registrierung erfolgreich. Bitte einloggen.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Ungültige Anmeldedaten', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if current_user.role != 'student':
        flash('Nur Fahrschüler können Bilder hochladen.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        if not request.form.get('accept'):
            flash('Du musst den Datenschutzbestimmungen zustimmen.', 'danger')
            return redirect(url_for('upload'))
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            img = Image(filename=filename, user_id=current_user.id)
            db.session.add(img)
            db.session.commit()
            flash('Bild hochgeladen. Wird nach Prüfung freigeschaltet.')
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/rate', methods=['GET', 'POST'])
@login_required
def rate():
    if current_user.role != 'student':
        flash('Nur Fahrschüler können Bewertungen abgeben.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        theory = int(request.form.get('theory'))
        driving = int(request.form.get('driving'))
        Rating.query.filter_by(user_id=current_user.id).delete()
        rating = Rating(theory=theory, driving=driving, user_id=current_user.id)
        db.session.add(rating)
        db.session.commit()
        flash('Bewertung gespeichert.')
        return redirect(url_for('index'))
    return render_template('rate.html')

@app.route('/teacher')
@login_required
def teacher():
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    images = Image.query.filter_by(approved=False).all()
    ratings = Rating.query.all()
    return render_template('teacher.html', images=images, ratings=ratings)

@app.route('/approve/<int:image_id>')
@login_required
def approve(image_id):
    if current_user.role != 'teacher':
        return redirect(url_for('index'))
    img = Image.query.get_or_404(image_id)
    img.approved = True
    db.session.commit()
    flash('Bild freigeschaltet.')
    return redirect(url_for('teacher'))

@app.route('/request_delete')
@login_required
def request_delete():
    current_user.deletion_requested_at = datetime.utcnow()
    db.session.commit()
    flash('Dein Konto wird in 24 Stunden gelöscht.')
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
