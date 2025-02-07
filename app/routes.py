from flask import Blueprint, jsonify, request
from app.services.data_collector import collect_data
from app.services.google_custom_search import get_snippet  # OpenAI API 호출이 포함됨
from app.services.recommender import recommend

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

    # 네이버 API에서 기본 데이터 수집
    collected_data = collect_data(location, category)

    enriched_results = []

    for item in collected_data:  # collected_data는 리스트여야 함
        description_data = get_snippet(
            category=item["category"],
            name=item["name"],
            address=item["address"],
            link=item["link"]  # 원래의 링크 전달
        )
        enriched_results.append(description_data)

    return jsonify({"code": "SU", "message": "Success.", "results": enriched_results})

# Blueprint 추가
recommendation_bp = Blueprint("recommendation", __name__)

@recommendation_bp.route("/recommend", methods=["POST"])
def get_recommendation():
    data = request.get_json()
    schedule = data.get("schedule")
    event_list = data.get("event_list")

    if not schedule or not event_list:
        return jsonify({"code": "VF", "message": "Validation failed. Schedule and event_list are required."}), 400

    recommendation = recommend(schedule, event_list)
    return jsonify({"code": "SU", "message": "Success.", "result": recommendation})
