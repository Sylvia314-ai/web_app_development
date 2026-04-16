import random
from flask import Blueprint, render_template, redirect, url_for, request, session, flash, abort
from app.models.divination import DivinationRecord

divination_bp = Blueprint('divination', __name__, url_prefix='/divination')

# 六十甲子籤詩資料（精簡版，可自行擴充）
FORTUNE_DATA = {
    '抽籤': [
        {
            'title': '上上籤 — 花開富貴',
            'content': '此籤象徵鴻運當頭，萬事如意。所求之事皆可成就，財運亨通，家宅平安。宜積極進取，把握良機，吉星高照，諸事順遂。'
        },
        {
            'title': '上籤 — 風調雨順',
            'content': '此籤顯示時運漸佳，凡事循序漸進必有所成。感情順遂，事業穩健上升。需保持耐心，勿躁進，水到渠成之象。'
        },
        {
            'title': '中籤 — 守成待時',
            'content': '此籤指示目前宜守不宜攻，靜待時機方為上策。需沉住氣，不宜輕舉妄動，虛心求教貴人，可逢凶化吉。'
        },
        {
            'title': '中下籤 — 霧裡看花',
            'content': '此籤顯示前路迷霧，需謹慎前行。財運稍弱，感情多波折。宜反躬自省、廣結善緣，持正心之人可得貴人相助。'
        },
        {
            'title': '下籤 — 逆水行舟',
            'content': '此籤警示近期多有阻礙，切勿強行蠻幹。宜靜心修身、廣積陰德，轉化逆境。万事忍讓，靜待風雨過後天晴。'
        },
    ],
    '塔羅': [
        {
            'title': '愚者 (The Fool) — 新的旅程',
            'content': '愚者代表全新的開始與無限的可能。你正站在生命的轉捩點，帶著純真的心出發。放下對未來的恐懼，勇於嘗試，旅程中將遇見意想不到的驚喜。'
        },
        {
            'title': '魔術師 (The Magician) — 意志與行動',
            'content': '你擁有實現夢想所需的全部工具與才能。魔術師告訴你，時機已到，現在正是採取行動、將想法化為現實的最佳時刻。相信自己的能力。'
        },
        {
            'title': '女祭司 (The High Priestess) — 直覺與洞察',
            'content': '內在的智慧正引領你。此刻需要靜下心來傾聽直覺，答案不在外部的喧囂中，而在你心靈深處的寧靜裡。守護內心的秘密與知識。'
        },
        {
            'title': '命運之輪 (Wheel of Fortune) — 轉機',
            'content': '命運的輪盤正在轉動，好運與機遇即將來臨。接受生命中的循環變化，順應天道，此刻正是你的轉運之時。把握命運帶來的新機遇。'
        },
        {
            'title': '星星 (The Star) — 希望與療癒',
            'content': '經歷風雨後，星星帶來希望與療癒的曙光。前方充滿光明，相信宇宙的美好安排。你的願望與夢想正在逐漸成形，保持信心與感恩之心。'
        },
    ],
}

@divination_bp.route('/')
def index():
    """顯示可選擇的算命種類。"""
    divination_types = list(FORTUNE_DATA.keys())
    return render_template('divination/index.html', divination_types=divination_types)

@divination_bp.route('/draw', methods=['POST'])
def draw():
    """
    接收算命種類，隨機產生結果，存入 DB 並重導向至結果頁面。
    需要登入才能儲存紀錄。
    """
    if not session.get('user_id'):
        flash('請先登入才能使用算命功能。', 'warning')
        return redirect(url_for('auth.login'))

    divination_type = request.form.get('divination_type', '').strip()

    if not divination_type or divination_type not in FORTUNE_DATA:
        flash('無效的算命類型，請重新選擇。', 'danger')
        return redirect(url_for('divination.index'))

    # 隨機從對應的算命資料中抽一筆
    fortune = random.choice(FORTUNE_DATA[divination_type])

    record_id = DivinationRecord.create({
        'user_id': session['user_id'],
        'type': divination_type,
        'result_title': fortune['title'],
        'result_content': fortune['content'],
    })

    if record_id:
        return redirect(url_for('divination.result', record_id=record_id))
    else:
        flash('抽籤過程發生錯誤，請稍後再試。', 'danger')
        return redirect(url_for('divination.index'))

@divination_bp.route('/result/<int:record_id>')
def result(record_id):
    """
    根據 record_id 查詢算命結果，並驗證是否為本人的紀錄。
    """
    if not session.get('user_id'):
        flash('請先登入才能查看結果。', 'warning')
        return redirect(url_for('auth.login'))

    record = DivinationRecord.get_by_id(record_id)

    if not record:
        abort(404)

    # 確認這筆紀錄是否屬於當前登入的使用者
    if record['user_id'] != session['user_id']:
        abort(403)

    return render_template('divination/result.html', record=record)

@divination_bp.route('/history')
def history():
    """顯示當前使用者過去的所有算命紀錄。"""
    if not session.get('user_id'):
        flash('請先登入才能查看歷史紀錄。', 'warning')
        return redirect(url_for('auth.login'))

    records = DivinationRecord.get_by_user_id(session['user_id'])
    return render_template('divination/history.html', records=records)
