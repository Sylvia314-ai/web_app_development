from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    HTTP Method: GET, POST
    Logic: 
        GET: 顯示註冊表單。
        POST: 接收註冊表單資料，檢查帳號及信箱是否重複，將密碼 Hash 後存入 DB。
    Output:
        GET: 渲染 templates/auth/register.html
        POST: 成功後重導至 /auth/login
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    HTTP Method: GET, POST
    Logic:
        GET: 顯示登入表單。
        POST: 驗證帳號密碼，成功後將 user_id 存入 Session。
    Output:
        GET: 渲染 templates/auth/login.html
        POST: 成功後重導至首頁 (/)，失敗則顯示錯誤 Flash Message 停留在原頁
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    HTTP Method: GET
    Logic: 清除 session 中的登入狀態。
    Output: 重導至首頁 (/)
    """
    pass
