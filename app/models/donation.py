from .db import get_db_connection

class Donation:
    @staticmethod
    def create(data):
        """
        新增一筆捐項紀錄。
        參數:
          data (dict): 包含 user_id, amount, status(選填, 預設'pending')
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO donations (user_id, amount, status) VALUES (?, ?, ?)',
                (data.get('user_id'), data.get('amount'), data.get('status', 'pending'))
            )
            conn.commit()
            lastrowid = cursor.lastrowid
            conn.close()
            return lastrowid
        except Exception as e:
            print(f"Error creating donation: {e}")
            return None

    @staticmethod
    def get_by_id(item_id):
        """取得單筆捐款記錄。"""
        try:
            conn = get_db_connection()
            donation = conn.execute('SELECT * FROM donations WHERE id = ?', (item_id,)).fetchone()
            conn.close()
            return dict(donation) if donation else None
        except Exception as e:
            print(f"Error getting donation by id: {e}")
            return None
        
    @staticmethod
    def get_by_user_id(user_id):
        """取得特定使用者的捐款。"""
        try:
            conn = get_db_connection()
            donations = conn.execute('SELECT * FROM donations WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
            conn.close()
            return [dict(d) for d in donations]
        except Exception as e:
            print(f"Error getting donations by user_id: {e}")
            return []

    @staticmethod
    def get_all():
        """取得所有記錄。"""
        try:
            conn = get_db_connection()
            donations = conn.execute('SELECT * FROM donations ORDER BY created_at DESC').fetchall()
            conn.close()
            return [dict(d) for d in donations]
        except Exception as e:
            print(f"Error getting all donations: {e}")
            return []

    @staticmethod
    def update(item_id, data):
        """更新訂單狀態"""
        try:
            conn = get_db_connection()
            if 'status' in data:
                conn.execute('UPDATE donations SET status = ? WHERE id = ?', (data['status'], item_id))
                conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating donation: {e}")
            return False

    @staticmethod
    def delete(item_id):
        """刪除單筆記錄。"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM donations WHERE id = ?', (item_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting donation: {e}")
            return False
