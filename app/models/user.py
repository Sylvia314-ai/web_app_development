from .db import get_db_connection

class User:
    @staticmethod
    def create(data):
        """
        新增一筆使用者記錄。
        參數：
          data (dict): 包含 username, email, password_hash
        回傳：
          int: 新增的紀錄 ID，若失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (data.get('username'), data.get('email'), data.get('password_hash'))
            )
            conn.commit()
            lastrowid = cursor.lastrowid
            conn.close()
            return lastrowid
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_by_id(item_id):
        """
        根據 ID 取得單筆使用者記錄。
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (item_id,)).fetchone()
            conn.close()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None

    @staticmethod
    def get_by_username(username):
        """
        根據 username 取得使用者記錄。
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            conn.close()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有使用者記錄。"""
        try:
            conn = get_db_connection()
            users = conn.execute('SELECT * FROM users').fetchall()
            conn.close()
            return [dict(u) for u in users]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    @staticmethod
    def update(item_id, data):
        """
        更新單筆使用者記錄。
        參數：
          item_id (int): 使用者 ID
          data (dict): 包含需要更新的欄位 (目前支援 email, password_hash)
        """
        try:
            conn = get_db_connection()
            query = "UPDATE users SET "
            params = []
            updates = []
            
            if 'email' in data:
                updates.append("email = ?")
                params.append(data['email'])
            if 'password_hash' in data:
                updates.append("password_hash = ?")
                params.append(data['password_hash'])
                
            if updates:
                query += ", ".join(updates) + " WHERE id = ?"
                params.append(item_id)
                conn.execute(query, tuple(params))
                conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    @staticmethod
    def delete(item_id):
        """刪除單筆使用者記錄。"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE id = ?', (item_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
