from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.models.donation import Donation

donation_bp = Blueprint('donation', __name__, url_prefix='/donation')

# 捐款金額選項（台幣）
DONATION_OPTIONS = [50, 100, 200, 500, 1000]

@donation_bp.route('/')
def donate():
    """顯示捐款金額選擇表單。"""
    return render_template('donation/donate.html', donation_options=DONATION_OPTIONS)

@donation_bp.route('/donate', methods=['POST'])
def process_donate():
    """
    接收捐款金額，建立捐款紀錄（模擬），重導向至成功頁。
    """
    if not session.get('user_id'):
        flash('請先登入才能進行線上捐獻。', 'warning')
        return redirect(url_for('auth.login'))

    amount_str = request.form.get('amount', '').strip()

    # 驗證金額
    if not amount_str:
        flash('請選擇捐款金額。', 'danger')
        return redirect(url_for('donation.donate'))

    try:
        amount = int(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash('捐款金額無效，請重新選擇。', 'danger')
        return redirect(url_for('donation.donate'))

    # 建立捐款紀錄，模擬直接完成支付
    donation_id = Donation.create({
        'user_id': session['user_id'],
        'amount': amount,
        'status': 'completed',  # MVP 模擬：直接標記為成功
    })

    if donation_id:
        # 將金額存入 session 供感謝頁面顯示
        session['last_donation_amount'] = amount
        return redirect(url_for('donation.success'))
    else:
        flash('捐款過程發生錯誤，請稍後再試。', 'danger')
        return redirect(url_for('donation.donate'))

@donation_bp.route('/success')
def success():
    """顯示捐款成功與祈福感謝頁面。"""
    amount = session.pop('last_donation_amount', None)
    return render_template('donation/success.html', amount=amount)
