import os
from flask import Flask

def create_app():
    # 建立與設定 Flask App
    app = Flask(__name__)
    
    # 載入設定 (SECRET_KEY 用於 flash message)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # 初始化資料庫
    from .models.task import Task
    with app.app_context():
        Task.init_db()

    # 註冊 Blueprints (路由)
    from .routes.task_routes import task_bp
    app.register_blueprint(task_bp)

    return app
