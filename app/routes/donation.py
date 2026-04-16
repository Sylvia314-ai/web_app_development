from flask import Blueprint

donation_bp = Blueprint('donation', __name__, url_prefix='/donation')

@donation_bp.route('/')
def donate():
    """
    HTTP Method: GET
    Logic: 顯示捐獻金額方案及祈福內容填寫表單。
    Output: 渲染 templates/donation/donate.html
    """
    pass

@donation_bp.route('/donate', methods=['POST'])
def process_donate():
    """
    HTTP Method: POST
    Logic: 接收捐款表單之金額等資料，建立一筆捐款紀錄至 DB。
    Output: 重導至 /donation/success
    """
    pass

@donation_bp.route('/success')
def success():
    """
    HTTP Method: GET
    Logic: 顯示捐獻成功與祈福感謝訊息。
    Output: 渲染 templates/donation/success.html
    """
    pass
