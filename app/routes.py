from flask import Blueprint, jsonify, request
from app.services.data_collector import collect_data

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

# data_collector Blueprint 추가
data_collector_bp = Blueprint("data_collector", __name__)

@data_collector_bp.route("/data/collector", methods=["POST"])
def get_collected_data():
    data = request.get_json()
    location = data.get("location")
    category = data.get("category")

    if not location or not category:
        return jsonify({"code": "VF", "message": "Validation failed. Location and category are required."}), 400

    response = collect_data(location, category)
    return jsonify(response)
