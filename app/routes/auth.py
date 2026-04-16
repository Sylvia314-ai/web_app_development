import hashlib
from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def hash_password(password):
    """使用 SHA-256 將密碼進行雜湊加密。"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_password(password, password_hash):
    """比對密碼與雜湊值是否相符。"""
    return hash_password(password) == password_hash

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: 顯示註冊表單。
    POST: 接收表單資料，驗證後寫入 DB。
    """
    if session.get('user_id'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # 必填欄位驗證
        if not username or not email or not password:
            flash('請填寫所有必填欄位。', 'danger')
            return render_template('auth/register.html')

        # 帳號長度限制
        if len(username) < 3:
            flash('帳號名稱至少需要 3 個字元。', 'danger')
            return render_template('auth/register.html')

        # 密碼長度限制
        if len(password) < 6:
            flash('密碼至少需要 6 個字元。', 'danger')
            return render_template('auth/register.html')

        # 確認帳號是否重複
        if User.get_by_username(username):
            flash('此帳號名稱已被使用，請選擇其他名稱。', 'danger')
            return render_template('auth/register.html')

        # 建立使用者
        password_hash = hash_password(password)
        user_id = User.create({
            'username': username,
            'email': email,
            'password_hash': password_hash
        })

        if user_id:
            flash('註冊成功！請登入。', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('註冊失敗，此電子信箱可能已被使用，請稍後再試。', 'danger')
            return render_template('auth/register.html')

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 顯示登入表單。
    POST: 驗證帳號密碼並建立 Session。
    """
    if session.get('user_id'):
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('請輸入帳號與密碼。', 'danger')
            return render_template('auth/login.html')

        user = User.get_by_username(username)

        if user and check_password(password, user['password_hash']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'歡迎回來，{user["username"]}！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('帳號或密碼有誤，請重新嘗試。', 'danger')
            return render_template('auth/login.html')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """清除 Session 並重導至首頁。"""
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('main.index'))
