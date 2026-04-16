from flask import Blueprint

divination_bp = Blueprint('divination', __name__, url_prefix='/divination')

@divination_bp.route('/')
def index():
    """
    HTTP Method: GET
    Logic: 列出可供選擇的算命種類（例如籤筒、塔羅牌）。
    Output: 渲染 templates/divination/index.html
    """
    pass

@divination_bp.route('/draw', methods=['POST'])
def draw():
    """
    HTTP Method: POST
    Logic: 
        接收所選的算命類型，從後端隨機產生抽籤結果，
        將結果與當前 user_id 呼叫 DivinationRecord.create() 存回資料庫。
    Output: 重導至 /divination/result/<id>
    """
    pass

@divination_bp.route('/result/<int:record_id>')
def result(record_id):
    """
    HTTP Method: GET
    Logic: 根據傳入的 record_id 查詢對應的結果，並驗證該結果是否屬於登入者。
    Output: 渲染 templates/divination/result.html
    """
    pass

@divination_bp.route('/history')
def history():
    """
    HTTP Method: GET
    Logic: 取得當前使用者過去所有的算命紀錄 (DivinationRecord.get_by_user_id)。
    Output: 渲染 templates/divination/history.html
    """
    pass
