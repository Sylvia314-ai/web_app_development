from .db import get_db_connection

class DivinationRecord:
    @staticmethod
    def create(data):
        """
        新增一筆算命紀錄。
        參數：
          data (dict): 包含 user_id, type, result_title, result_content
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO divination_records (user_id, type, result_title, result_content) VALUES (?, ?, ?, ?)',
                (data.get('user_id'), data.get('type'), data.get('result_title'), data.get('result_content'))
            )
            conn.commit()
            lastrowid = cursor.lastrowid
            conn.close()
            return lastrowid
        except Exception as e:
            print(f"Error creating divination record: {e}")
            return None

    @staticmethod
    def get_by_id(item_id):
        """根據 ID 取得單筆記錄。"""
        try:
            conn = get_db_connection()
            record = conn.execute('SELECT * FROM divination_records WHERE id = ?', (item_id,)).fetchone()
            conn.close()
            return dict(record) if record else None
        except Exception as e:
            print(f"Error getting divination record by id: {e}")
            return None
        
    @staticmethod
    def get_by_user_id(user_id):
        """取得特定使用者的所有紀錄。"""
        try:
            conn = get_db_connection()
            records = conn.execute('SELECT * FROM divination_records WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
            conn.close()
            return [dict(r) for r in records]
        except Exception as e:
            print(f"Error getting divination records by user_id: {e}")
            return []

    @staticmethod
    def get_all():
        """取得所有記錄。"""
        try:
            conn = get_db_connection()
            records = conn.execute('SELECT * FROM divination_records ORDER BY created_at DESC').fetchall()
            conn.close()
            return [dict(r) for r in records]
        except Exception as e:
            print(f"Error getting all divination records: {e}")
            return []

    @staticmethod
    def update(item_id, data):
        """
        更新記錄。
        參數：
          item_id (int): 記錄 ID
          data (dict): 包含 result_title, result_content 作為更新內容
        """
        try:
            conn = get_db_connection()
            query = "UPDATE divination_records SET "
            params = []
            updates = []
            
            if 'result_title' in data:
                updates.append("result_title = ?")
                params.append(data['result_title'])
            if 'result_content' in data:
                updates.append("result_content = ?")
                params.append(data['result_content'])
                
            if updates:
                query += ", ".join(updates) + " WHERE id = ?"
                params.append(item_id)
                conn.execute(query, tuple(params))
                conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating divination record: {e}")
            return False

    @staticmethod
    def delete(item_id):
        """刪除單筆記錄。"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM divination_records WHERE id = ?', (item_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting divination record: {e}")
            return False
