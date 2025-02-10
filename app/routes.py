from flask import Blueprint, jsonify, request
from app.services.data_collector import collect_data
from app.services.google_custom_search import get_snippet
from app.services.openai_processor import generate_description
from app.services.recommender import recommend


api_bp = Blueprint('api', __name__)

@api_bp.route('/ai/recommendation', methods=['POST'])
def run_main():
    data = request.get_json()

    location = data.get("location")
    free_time = data.get("free_time")
    category = data.get("category")

    if not location or not free_time or not category:
        return jsonify({"code": "VF", "message": "Validation failed. Location, free_time and category are required."}), 400

    # 네이버 API에서 기본 데이터 수집
    collected_data = collect_data(location, category)

    if isinstance(collected_data, dict):
        return jsonify({"code": "SE", "message": "시스템 에러. 관리자에게 문의하세요."}), 400

    event_list = []
    for item in collected_data:  # collected_data는 리스트여야 함
        category = item["category"]
        title = item["title"]
        address = item["address"]
        url = item["link"]

        snippets = get_snippet(
            category=category,
            title=title,
            place='',
        )

        full_data = generate_description(
            category=category, 
            title=title, 
            place='', 
            address=address, 
            period='', 
            opening_time='', 
            url=url, 
            snippets=snippets)
        
        event_list.append(full_data)

    recommendation = recommend(free_time, event_list)

    if recommendation['title'] == "None":
        return jsonify({"code": "NOT FOUND", "message": "No data available for the given criteria."})

    return jsonify({"code": "SU", "message": "Success.", "result": recommendation})
