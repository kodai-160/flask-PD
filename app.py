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
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    comments = db.relationship('Comment', backref='author', lazy=True)
    stamps = db.relationship('Stamp', backref='user', lazy=True)  # lazy='dynamic'からlazy=Trueへ変更

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Stamp(db.Model):
    __tablename__ = 'stamps'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    collected = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 外部キーの追加

    def __repr__(self):
        return f'<Stamp {self.name}>'
    
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
        # パスワードのハッシュ化(推奨)
        #hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(name=name, email=email, password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
            
            # 新しいユーザーのスタンプをFalseで初期化
            initialize_stamps_for_user(new_user)

            # 登録成功後の処理 (ログインページへリダイレクトなど)
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            return "このメールアドレスは既に登録されています。"

    return render_template('register.html')

def initialize_stamps_for_user(user):
    stamp_names = ['stamp1', 'stamp2', 'stamp3', 'stamp4', 'stamp5', 'stamp6', 'stamp7', 'stamp8', 'stamp9']
    for name in stamp_names:
        new_stamp = Stamp(name=name, collected=False, user_id=user.id)
        db.session.add(new_stamp)
    db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=name, password=password).first()

        if user:
            login_user(user)
            return redirect(url_for('stamp_rally_moring'))
        else:
            return "Failed Login"

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/stamp_rally_morning')
@login_required
def stamp_rally_morning():
    # 現在のユーザーに関連するスタンプを取得
    user_stamps = Stamp.query.filter_by(user_id=current_user.id).all()
    # スタンプの状態を辞書として抽出
    stamps_status = {stamp.name: stamp.collected for stamp in user_stamps}
    # テンプレートにスタンプの状態を渡す
    return render_template('stamp_rally_morning.html', stamps_status=stamps_status)

@app.route('/stamp_rally_noon')
def stamp_rally_noon():
    # 現在のユーザーに関連するスタンプを取得
    user_stamps = Stamp.query.filter_by(user_id=current_user.id).all()
    # スタンプの状態を辞書として抽出
    stamps_status = {stamp.name: stamp.collected for stamp in user_stamps}
    # テンプレートにスタンプの状態を渡す
    return render_template('stamp_rally_noon.html', stamps_status=stamps_status)

@app.route('/stamp_rally_night')
def stamp_rally_night():
    # 現在のユーザーに関連するスタンプを取得
    user_stamps = Stamp.query.filter_by(user_id=current_user.id).all()
    # スタンプの状態を辞書として抽出
    stamps_status = {stamp.name: stamp.collected for stamp in user_stamps}
    # テンプレートにスタンプの状態を渡す
    return render_template('stamp_rally_night.html', stamps_status=stamps_status)

@app.route('/morning/stamp1')
def stamp1():
    comments = Comment.query.all()
    return render_template('/morning/stamp1.html', comments=comments)

@app.route('/morning/stamp2')
def stamp2():
    comments = Comment.query.all()
    return render_template('/morning/stamp2.html', comments=comments)

@app.route('/morning/stamp3')
def stamp3():
    comments = Comment.query.all()
    return render_template('/morning/stamp3.html', comments=comments)

@app.route('/morning/stamp4')
def stamp4():
    comments = Comment.query.all()
    return render_template('/morning/stamp4.html', comments=comments)

@app.route('/morning/stamp5')
def stamp5():
    comments = Comment.query.all()
    return render_template('/morning/stamp5.html', comments=comments)

@app.route('/morning/stamp6')
def stamp6():
    comments = Comment.query.all()
    return render_template('/morning/stamp6.html', comments=comments)

@app.route('/morning/stamp7')
def stamp7():
    comments = Comment.query.all()
    return render_template('/morning/stamp7.html', comments=comments)

@app.route('/morning/stamp8')
def stamp8():
    comments = Comment.query.all()
    return render_template('/morning/stamp8.html', comments=comments)

@app.route('/morning/stamp9')
def stamp9():
    comments = Comment.query.all()
    return render_template('/morning/stamp9.html', comments=comments)

@app.route('/noon/stamp1')
def noon_stamp1():
    comments = Comment.query.all()
    return render_template('/noon/stamp1.html', comments=comments)

@app.route('/noon/stamp2')
def noon_stamp2():
    comments = Comment.query.all()
    return render_template('/noon/stamp2.html', comments=comments)

@app.route('/noon/stamp3')
def noon_stamp3():
    comments = Comment.query.all()
    return render_template('/noon/stamp3.html', comments=comments)

@app.route('/noon/stamp4')
def noon_stamp4():
    comments = Comment.query.all()
    return render_template('/noon/stamp4.html', comments=comments)

@app.route('/noon/stamp5')
def noon_stamp5():
    comments = Comment.query.all()
    return render_template('/noon/stamp5.html', comments=comments)

@app.route('/noon/stamp6')
def noon_stamp6():
    comments = Comment.query.all()
    return render_template('/noon/stamp6.html', comments=comments)

@app.route('/noon/stamp7')
def noon_stamp7():
    comments = Comment.query.all()
    return render_template('/noon/stamp7.html', comments=comments)

@app.route('/noon/stamp8')
def noon_stamp8():
    comments = Comment.query.all()
    return render_template('/noon/stamp8.html', comments=comments)

@app.route('/noon/stamp9')
def noon_stamp9():
    comments = Comment.query.all()
    return render_template('/noon/stamp9.html', comments=comments)

@app.route('/night/stamp1')
def night_stamp1():
    comments = Comment.query.all()
    return render_template('/night/stamp1.html', comments=comments)

@app.route('/night/stamp2')
def night_stamp2():
    comments = Comment.query.all()
    return render_template('/night/stamp2.html', comments=comments)

@app.route('/night/stamp3')
def night_stamp3():
    comments = Comment.query.all()
    return render_template('/night/stamp3.html', comments=comments)

@app.route('/night/stamp4')
def night_stamp4():
    comments = Comment.query.all()
    return render_template('/night/stamp4.html', comments=comments)

@app.route('/night/stamp5')
def night_stamp5():
    comments = Comment.query.all()
    return render_template('/night/stamp5.html', comments=comments)

@app.route('/night/stamp6')
def night_stamp6():
    comments = Comment.query.all()
    return render_template('/night/stamp6.html', comments=comments)

@app.route('/night/stamp7')
def night_stamp7():
    comments = Comment.query.all()
    return render_template('/night/stamp7.html', comments=comments)

@app.route('/night/stamp8')
def night_stamp8():
    comments = Comment.query.all()
    return render_template('/night/stamp8.html', comments=comments)

@app.route('/night/stamp9')
def night_stamp9():
    comments = Comment.query.all()
    return render_template('/night/stamp9.html', comments=comments)


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if request.method == 'POST':
        comment_text = request.form['comment']
        comment_date = datetime.now()
        # 現在ログインしているユーザーのIDを使用
        new_comment = Comment(user_id=current_user.id, comment=comment_text, comment_date=comment_date)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('stamp1'))
    
@app.route('/update_stamp', methods=['POST'])
@login_required
def update_stamp():
    name = request.form.get('name')
    if name:
        stamp = Stamp.query.filter_by(name=name, user_id=current_user.id).first()
        if stamp and not stamp.collected:
            stamp.collected = True
            db.session.commit()
            return jsonify({'message': 'Stamp updated.', 'collected': stamp.collected}), 200
        elif stamp and stamp.collected:
            return jsonify({'message': 'Stamp already collected.', 'collected': stamp.collected}), 409
        else:
            return jsonify({'message': 'Stamp not found.'}), 404
    else:
        return jsonify({'message': 'Invalid stamp name.'}), 400

@app.route('/get_stamps')
@login_required
def get_stamps():
    stamps = Stamp.query.filter_by(user_id=current_user.id).all()
    stamp_list = [{'name': stamp.name, 'collected': stamp.collected} for stamp in stamps]
    return jsonify(stamps=stamp_list)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
