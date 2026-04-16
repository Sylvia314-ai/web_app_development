from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    HTTP Method: GET
    Logic: 從 session 檢查登入狀態。首頁顯示每日運勢與功能捷徑。
    Output: 渲染 templates/index.html
    """
    pass
