from .db import get_db_connection

class Donation:
    @staticmethod
    def create(user_id, amount, status='pending'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO donations (user_id, amount, status) VALUES (?, ?, ?)',
            (user_id, amount, status)
        )
        conn.commit()
        lastrowid = cursor.lastrowid
        conn.close()
        return lastrowid

    @staticmethod
    def get_by_id(donation_id):
        conn = get_db_connection()
        donation = conn.execute('SELECT * FROM donations WHERE id = ?', (donation_id,)).fetchone()
        conn.close()
        return dict(donation) if donation else None
        
    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db_connection()
        donations = conn.execute('SELECT * FROM donations WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
        conn.close()
        return [dict(d) for d in donations]

    @staticmethod
    def get_all():
        conn = get_db_connection()
        donations = conn.execute('SELECT * FROM donations ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(d) for d in donations]

    @staticmethod
    def update_status(donation_id, status):
        conn = get_db_connection()
        conn.execute('UPDATE donations SET status = ? WHERE id = ?', (status, donation_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(donation_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM donations WHERE id = ?', (donation_id,))
        conn.commit()
        conn.close()
