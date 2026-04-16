from .db import get_db_connection

class DivinationRecord:
    @staticmethod
    def create(user_id, record_type, result_title, result_content):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO divination_records (user_id, type, result_title, result_content) VALUES (?, ?, ?, ?)',
            (user_id, record_type, result_title, result_content)
        )
        conn.commit()
        lastrowid = cursor.lastrowid
        conn.close()
        return lastrowid

    @staticmethod
    def get_by_id(record_id):
        conn = get_db_connection()
        record = conn.execute('SELECT * FROM divination_records WHERE id = ?', (record_id,)).fetchone()
        conn.close()
        return dict(record) if record else None
        
    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db_connection()
        records = conn.execute('SELECT * FROM divination_records WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
        conn.close()
        return [dict(r) for r in records]

    @staticmethod
    def get_all():
        conn = get_db_connection()
        records = conn.execute('SELECT * FROM divination_records ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(r) for r in records]

    @staticmethod
    def update(record_id, result_title=None, result_content=None):
        conn = get_db_connection()
        if result_title and result_content:
            conn.execute('UPDATE divination_records SET result_title = ?, result_content = ? WHERE id = ?', (result_title, result_content, record_id))
        elif result_title:
            conn.execute('UPDATE divination_records SET result_title = ? WHERE id = ?', (result_title, record_id))
        elif result_content:
            conn.execute('UPDATE divination_records SET result_content = ? WHERE id = ?', (result_content, record_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(record_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM divination_records WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()
