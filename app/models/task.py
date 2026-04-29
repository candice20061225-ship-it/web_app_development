import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

@contextmanager
def get_db_connection():
    """取得資料庫連線，並回傳支援字典存取的 Row"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    except sqlite3.Error as e:
        print(f"資料庫錯誤: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

class Task:
    @staticmethod
    def init_db():
        """初始化資料表，讀取 schema.sql 並執行"""
        schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            try:
                with get_db_connection() as conn:
                    conn.executescript(schema_sql)
                    conn.commit()
            except sqlite3.Error as e:
                print(f"初始化資料表失敗: {e}")

    @staticmethod
    def create(data):
        """新增一筆讀書任務
        :param data: dict，包含 subject, title, due_date
        :return: int, 新增的資料 ID (若失敗則回傳 None)
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO tasks (subject, title, due_date)
                    VALUES (?, ?, ?)
                ''', (data.get('subject'), data.get('title'), data.get('due_date')))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"建立任務失敗: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有讀書任務，依日期排序
        :return: list of sqlite3.Row
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM tasks
                    ORDER BY due_date ASC, created_at DESC
                ''')
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"查詢任務列表失敗: {e}")
            return []

    @staticmethod
    def get_by_id(task_id):
        """依據 ID 取得單一讀書任務
        :param task_id: int
        :return: sqlite3.Row 或是 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"查詢單一任務失敗: {e}")
            return None

    @staticmethod
    def update(task_id, data):
        """更新任務內容
        :param task_id: int
        :param data: dict，包含 subject, title, due_date
        :return: bool，表示是否成功
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE tasks
                    SET subject = ?, title = ?, due_date = ?
                    WHERE id = ?
                ''', (data.get('subject'), data.get('title'), data.get('due_date'), task_id))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"更新任務失敗: {e}")
            return False

    @staticmethod
    def toggle_status(task_id):
        """切換任務完成狀態 (0 -> 1, 1 -> 0)
        :param task_id: int
        :return: bool，表示是否成功
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE tasks
                    SET is_completed = CASE WHEN is_completed = 1 THEN 0 ELSE 1 END
                    WHERE id = ?
                ''', (task_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"更新任務狀態失敗: {e}")
            return False

    @staticmethod
    def delete(task_id):
        """刪除任務
        :param task_id: int
        :return: bool，表示是否成功
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"刪除任務失敗: {e}")
            return False
