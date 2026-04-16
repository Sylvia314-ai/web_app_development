from .db import get_db_connection

class User:
    @staticmethod
    def create(username, email, password_hash):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        lastrowid = cursor.lastrowid
        conn.close()
        return lastrowid

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None
        
    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_all():
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return [dict(u) for u in users]

    @staticmethod
    def update(user_id, email=None, password_hash=None):
        conn = get_db_connection()
        if email and password_hash:
            conn.execute('UPDATE users SET email = ?, password_hash = ? WHERE id = ?', (email, password_hash, user_id))
        elif email:
            conn.execute('UPDATE users SET email = ? WHERE id = ?', (email, user_id))
        elif password_hash:
            conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (password_hash, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
