from flask import Blueprint, render_template, request, redirect, url_for, jsonify

# 建立 Blueprint，方便管理路由
task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁，包含所有的任務清單與新增表單。
    """
    pass

@task_bp.route('/tasks/add', methods=['POST'])
def add_task():
    """
    接收新增任務的表單資料，並存入資料庫。
    成功後重導向回首頁。
    """
    pass

@task_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    切換指定任務的完成狀態。
    由於前端使用 AJAX 呼叫，應回傳 JSON 格式的成功與否狀態。
    """
    pass

@task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    刪除指定的任務。
    成功後重導向回首頁。
    """
    pass

@task_bp.route('/stats', methods=['GET'])
def stats():
    """
    顯示任務完成率與學習進度統計頁面。
    """
    pass
