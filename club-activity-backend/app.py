import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 导入模型（必须在 db 初始化之后）
from models.user import User
from models.club import Club
from models.event import Event
from models.registration import Registration

# 导入路由
from routes.auth import auth_bp
from routes.clubs import club_bp
from routes.events import event_bp
from routes.registrations import registration_bp

# 注册蓝图
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(club_bp, url_prefix='/api/clubs')
app.register_blueprint(event_bp, url_prefix='/api/events')
app.register_blueprint(registration_bp, url_prefix='/api/registrations')

# 创建数据库表（开发用）
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)