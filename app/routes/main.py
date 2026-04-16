from flask import Blueprint, render_template, redirect, url_for, session, flash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    HTTP Method: GET
    Logic: 從 session 檢查登入狀態。首頁顯示每日運勢與功能捷徑。
    Output: 渲染 templates/index.html
    """
    user_id = session.get('user_id')
    return render_template('index.html', user_id=user_id)
