from app import create_app

# 애플리케이션 생성
app = create_app()

if __name__ == "__main__":
    # Flask 서버 실행
    app.run(host="0.0.0.0", port=5000)

