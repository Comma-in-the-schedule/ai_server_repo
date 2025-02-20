from flask import Blueprint, jsonify, request
from app.services.data_collectors.naver_collector import collect_data
from app.services.snippets_collector import get_snippet
from app.services.description_generator import generate_description
from app.services.period_processor import is_free_time_in_period
from app.services.recommender import recommend

def process_popupstore(location, free_time):
    result = collect_data(location, "팝업스토어")

    if result["code"] != "SU":
        # return {"code": "SE", "message": f"system_error: N-{result['code']}"}
        return result
    
    elif not result["message"]:
        return {"code": "NF", "message": "No data found for the given criteria."}
    
    else:
        collected_data = result["message"]

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
            return {"code": "SE", "message": f"system_error: G-{snippets['code']}"}
        
        full_data = generate_description(
            category=category, 
            title=title, 
            place='', 
            address=address, 
            period='', 
            opening_time='', 
            url=url, 
            snippets=snippets["message"])

        if is_free_time_in_period(free_time, full_data['period']) or not full_data['period']:  # 운영 기간이 여가 시간에 포함될 경우, 운영 기간 데이터가 없을 경우에만 추가
            event_list.append(full_data)

    return {"code": "SU", "message": "Success.", "result": event_list}

def process_exhibition(location, free_time):
    # 테스트를 위한 임시 더미데이터
    event_list = [
        {
            "category": "전시회",
            "title": "데미데이터1",
            "description": "더미데이터1입니다.",
            "place": "장소1",
            "address": "서울특별시 강남구 ㅇㅇ로 ㅇㅇ길",
            "period": "2025.01.01.-2025.12.31.",
            "opening_time": "10:00-21:00",
            "url": "https://www.example1.com/"
        },
        {
            "category": "전시회",
            "title": "데미데이터2",
            "description": "더미데이터2입니다.",
            "place": "장소2",
            "address": "서울특별시 강남구 ㅁㅁ로 ㅁㅁ길",
            "period": "2025.01.10.-2025.12.13.",
            "opening_time": "09:00-19:00",
            "url": "https://www.example2.com/"
        }
    ]

    return {"code": "SU", "message": "Success.", "result": event_list}

api_bp = Blueprint('api', __name__)

@api_bp.route('/ai/recommendation', methods=['POST'])
def run_main():
    data = request.get_json()

    location = data.get("location")
    free_time = data.get("free_time")
    categories = data.get("category")  # 리스트 형태로 받을 수 있도록 수정

    if not location or not free_time or not categories:
        return jsonify({"code": "VF", "message": "Validation failed. Location, free_time and category are required."}), 400

    # category_nums가 단일 숫자(int)로 들어오면 리스트로 변환
    if isinstance(categories, int):
        categories = [categories]

    result_list = [["No Data"], ["No Data"]]

    for category in categories:
        # 네이버 API에서 기본 데이터 수집
        if category == 1:
            result = process_popupstore(location, free_time)
            if result["code"] == "SU":
                result_list[0] = result["result"]
            else:
                return jsonify(result)
        elif category == 2:
            result_list[1] = process_exhibition(location, free_time)["result"]

    return jsonify({"code": "SU", "message": "Success.", "result": result_list})
