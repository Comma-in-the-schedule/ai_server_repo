from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    # .env 파일 로드
    load_dotenv()

    # Flask 애플리케이션 생성
    app = Flask(__name__)

    # SECRET_KEY 설정 (환경 변수에서 가져오기)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_fallback_key')

    # Blueprint 등록
    from .routes import main
    app.register_blueprint(main)

    return app

