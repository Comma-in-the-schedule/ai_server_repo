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
    from .routes import api_bp  # recommendation_bp 추가
    '''
    google_custom_search.py, openai_processor.py의 blueprint를 지정하지 않는 이유
    - google_custom_search.py, openai_processor.py는 Flask 엔드포인트(API 엔드포인트)를 직접 제공하지
    않고, 비즈니스 로직(데이터 처리, API 요청 등)만 수행
    - routes.py에서 직접 해당 모듈의 함수를 호출하기 때문에 Flask 앱과 직접적인 연관이 없음
    '''
    app.register_blueprint(api_bp)

    return app
