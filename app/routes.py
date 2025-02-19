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
    category_nums = data.get("category")  # 리스트 형태로 받을 수 있도록 수정

    if not location or not free_time or not category_nums:
        return jsonify({"code": "VF", "message": "Validation failed. Location, free_time and category are required."}), 400

    # category_nums가 단일 숫자(int)로 들어오면 리스트로 변환
    if isinstance(category_nums, int):
        category_nums = [category_nums]

    category_list = {1: "팝업스토어", 2: "전시회", 3: "영화", 4: "공방"}
    
    collected_data = []
    
    for category_num in category_nums:
        category = category_list.get(category_num)

        if not category:
            continue  # 잘못된 카테고리 번호 무시
        
        # 네이버 API에서 기본 데이터 수집
        if category == "팝업스토어":
            data_result = collect_data(location, category)
        elif category == "전시회":
            data_result = {"code": "SU", "message": []}  # 다중 카테고리 반환 테스트 용. 전시회 데이터 없음 처리
        else:
            data_result = {"code": "SU", "message": []}  # 다중 카테고리 반환 테스트 용.

        if data_result["code"] != "SU":
            return jsonify({"code": "SE1", "message": f"system_error: N-{data_result['code']}"}), 400
        
        collected_data.extend(data_result["message"])

    if not collected_data:
        return jsonify({"code": "NF", "message": "No data found for the given criteria."})

    event_list = []
    for item in collected_data:
        category = item["category"]
        title = item["title"]
        address = item["address"]
        url = item["link"]

        snippets = get_snippet(
            category=category,
            title=title,
            place='',
        )

        if snippets["code"] != "SU":
            return jsonify({"code": "SE2", "message": f"system_error: G-{snippets['code']}"}), 400
        
        full_data = generate_description(
            category=category, 
            title=title, 
            place='', 
            address=address, 
            period='', 
            opening_time='', 
            url=url, 
            snippets=snippets["message"])
        
        event_list.append(full_data)

    recommendation = recommend(free_time, event_list)

    if recommendation[0]['title'] == "None":
        return jsonify({"code": "NF", "message": "No data found for the given criteria."})

    return jsonify({"code": "SU", "message": "Success.", "result": recommendation})
