import sqlite3
import os
from contextlib import contextmanager

# 資料庫檔案路徑，假設從專案根目錄執行 app.py
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

@contextmanager
def get_db_connection():
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓回傳結果可以像 dict 一樣透過欄位名稱存取
    try:
        yield conn
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
            with get_db_connection() as conn:
                conn.executescript(schema_sql)
                conn.commit()

    @staticmethod
    def create(subject, title, due_date):
        """新增一筆讀書任務"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (subject, title, due_date)
                VALUES (?, ?, ?)
            ''', (subject, title, due_date))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        """取得所有讀書任務，依日期排序"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM tasks
                ORDER BY due_date ASC, created_at DESC
            ''')
            return cursor.fetchall()

    @staticmethod
    def get_by_id(task_id):
        """依據 ID 取得單一讀書任務"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            return cursor.fetchone()

    @staticmethod
    def update(task_id, subject, title, due_date):
        """更新任務內容"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET subject = ?, title = ?, due_date = ?
                WHERE id = ?
            ''', (subject, title, due_date, task_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def toggle_status(task_id):
        """切換任務完成狀態 (0 -> 1, 1 -> 0)"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET is_completed = CASE WHEN is_completed = 1 THEN 0 ELSE 1 END
                WHERE id = ?
            ''', (task_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(task_id):
        """刪除任務"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            return cursor.rowcount > 0
