from flask import Blueprint, jsonify, request

# Blueprint 설정
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({'message': 'Welcome to the Flask AI Backend!'})

@main.route('/predict', methods=['POST'])
def predict():
    # 요청에서 데이터 가져오기
    data = request.get_json()

    # AI 모델 호출 (예제 로직)
    result = {"prediction": "example_output"}

    return jsonify(result)

