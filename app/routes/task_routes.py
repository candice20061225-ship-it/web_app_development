from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models.task import Task

# 建立 Blueprint，方便管理路由
task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁，包含所有的任務清單與新增表單。
    """
    tasks = Task.get_all()
    return render_template('index.html', tasks=tasks)

@task_bp.route('/tasks/add', methods=['POST'])
def add_task():
    """
    接收新增任務的表單資料，並存入資料庫。
    成功後重導向回首頁。
    """
    subject = request.form.get('subject', '').strip()
    title = request.form.get('title', '').strip()
    due_date = request.form.get('due_date', '').strip()
    
    # 基本的輸入驗證
    if not subject or not title or not due_date:
        flash('請填寫所有必填欄位 (科目、標題、預定日期)', 'danger')
        return redirect(url_for('task_bp.index'))
    
    data = {
        'subject': subject,
        'title': title,
        'due_date': due_date
    }
    
    task_id = Task.create(data)
    if task_id:
        flash('任務新增成功！', 'success')
    else:
        flash('新增任務失敗，請稍後再試。', 'danger')
        
    return redirect(url_for('task_bp.index'))

@task_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    切換指定任務的完成狀態。
    由於前端使用 AJAX 呼叫，應回傳 JSON 格式的成功與否狀態。
    """
    success = Task.toggle_status(task_id)
    
    # 判斷是否為 AJAX 請求 (Fetch/XHR)
    if request.headers.get('Content-Type') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': success})
    
    # 若為傳統表單請求
    if not success:
        flash('更新狀態失敗，找不到該任務', 'danger')
    return redirect(url_for('task_bp.index'))

@task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    刪除指定的任務。
    成功後重導向回首頁。
    """
    success = Task.delete(task_id)
    if success:
        flash('任務已成功刪除', 'success')
    else:
        flash('刪除失敗，找不到該任務', 'danger')
        
    return redirect(url_for('task_bp.index'))

@task_bp.route('/stats', methods=['GET'])
def stats():
    """
    顯示任務完成率與學習進度統計頁面。
    """
    tasks = Task.get_all()
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task['is_completed'])
    
    completion_rate = 0
    if total_tasks > 0:
        completion_rate = round((completed_tasks / total_tasks) * 100)
        
    return render_template('stats.html', 
                           total_tasks=total_tasks, 
                           completed_tasks=completed_tasks, 
                           completion_rate=completion_rate)
