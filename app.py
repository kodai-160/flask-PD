from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin, login_required
from werkzeug.security import generate_password_hash
import os
from datetime import datetime
from flask import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 秘密キーの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
class Comment(db.Model):
    tablename = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False)
    
class Stamp(db.Model):
    __tablename__ = 'stamp'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    station_name = db.Column(db.String(50), nullable=False)
    collected = db.Column(db.Boolean, default=False, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref=db.backref('stamps', lazy='dynamic'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # パスワードのハッシュ化(時間があったらエラー解決)
        # hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(name=name, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return "ユーザーを追加しました。"
        except IntegrityError:
            db.session.rollback()
            return "このメールアドレスは既に登録されています。"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=name, password=password).first()

        if user:
            login_user(user)
            return redirect(url_for('stamp'))
        else:
            return "Failed Login"

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/stamp')
@login_required
def stamp():
    return render_template('stamp_rally.html')

@app.route('/kenrokuen')
def kenrokuen():
    return render_template('kenrokuen.html')

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        comment_date = datetime.now()
        new_comment = Comment(user=name, comment=comment, comment_date=comment_date)
        db.session.add(new_comment)
        db.session.commit()
        # kenrokuen以外に設定する必要あり
        return redirect(url_for('kenrokuen')) 
    
@app.route('/update_stamp', methods=['POST'])
@login_required
def update_stamp():
    station_name = request.form['station']
    # 現在のユーザーのスタンプを検索または作成
    stamp = Stamp.query.filter_by(user_id=current_user.id, station_name=station_name).first()
    if not stamp:
        stamp = Stamp(user_id=current_user.id, station_name=station_name, collected=True)
        db.session.add(stamp)
    else:
        stamp.collected = True  # 既に存在する場合は、collectedをTrueに設定
    db.session.commit()
    return '', 204  # 成功した場合は204 No Contentを返す

@app.route('/get_stamps')
@login_required
def get_stamps():
    stamps = Stamp.query.filter_by(user_id=current_user.id).all()
    stamp_list = [{'station_name': stamp.station_name, 'collected': stamp.collected} for stamp in stamps]
    return jsonify(stamps=stamp_list)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
