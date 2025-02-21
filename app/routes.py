from flask import Blueprint, jsonify, request
from app.services.data_collectors.naver_collector import collect_data
from app.services.snippets_collector import get_snippet
from app.services.description_generator import generate_description
from app.services.period_processor import is_free_time_in_period, convert_to_period_format
from app.services.recommender import recommend
from app.services.data_collectors.exhibition_collector import fetch_exhibition_data


#test CI/CD
def process_popupstore(location, free_time):
    result = collect_data(location, "팝업스토어")

    if result["code"] != "SU":
        return {"code": "SE", "message": f"system_error: N-{result['code']}"}
    
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
        
        # 이미지 url 추가(추후 기능 구현)
        full_data["image"] = ""

        # 운영 기간이 여가 시간에 포함될 경우, 운영 기간 데이터가 없을 경우에만 추가
        if is_free_time_in_period(free_time, full_data['period']) or not full_data['period']:
            event_list.append(full_data)

    return {"code": "SU", "message": "Success.", "result": event_list}


# api 적용한 전시회
def process_exhibition(location, free_time):
    """
    사용자의 지역(location)과 여가 시간(free_time)에 맞는 전시회 데이터를 가져와 가공하는 함수.
    """
    """
    result = fetch_exhibition_data(location, free_time)

    if result["code"] != "SU":
        return jsonify(result)
    else:
        collected_data = result["message"]

    event_list = []
    for item in collected_data:
        title = item.get("title", "알 수 없음")
        place = item.get("place", "알 수 없음")
        address = item.get("area", "알 수 없음")
        period = convert_to_period_format(item.get('startDate', '미정'), {item.get('endDate', '미정')})
        image = item.get("thumbnail", "")

        # Snippets 가져오기
        snippets = get_snippet(category="전시회", title=title, place=place)
        snippet_texts = snippets["message"] if snippets["code"] == "SU" else []

        # OpenAI API를 이용해 description 생성
        full_data = generate_description(
            category="전시회",
            title=title,
            place=place,
            address=address,
            period=period,
            opening_time="",
            url="",
            snippets=snippet_texts
        )
        # image url을 추가
        full_data["image"] = image

        event_list.append(full_data)
    """
    event_list = """
    {
    "address": "서울특별시 강남구 OO로",
    "category": "전시회",
    "description": "더미 데이터 설명",
    "image": "",
    "opening_time": "00:00 - 00:00",
    "period": "0000.00.00.-0000.00.00.",
    "place": "장소",
    "title": "더미데이터입니다.",
    "url": "http://www.example.co.kr/"
    }
    """

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

    result_list = [["No Data"], ["No Data"]]

    for category in categories:
        if category == 1:
            result = process_popupstore(location, free_time)
            if result["code"] == "SU":
                result_list[0] = result["result"]
            else:
                return jsonify(result)

        elif category == 2:
            result = process_exhibition(location, free_time)
            if result["code"] == "SU":
                result_list[1] = result["result"]
            else:
                return jsonify(result)

    return jsonify({"code": "SU", "message": "Success.", "result": result_list})
