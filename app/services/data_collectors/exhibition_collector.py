import requests
import xmltodict
import os
from app.services.snippets_collector import get_snippet
from app.services.description_generator import generate_description

API_URL = "https://apis.data.go.kr/B553457/nopenapi/rest/publicperformancedisplays/realm"

SIDO_MAPPING = {
    "서울": "서울",
    "경기도": "경기"
}

def extract_sido(location):
    """ 사용자의 입력 지역에서 시/도 정보만 추출 """
    for key in SIDO_MAPPING:
        if key in location:
            return SIDO_MAPPING[key]
    return location.split()[0]  # 기본적으로 첫 번째 단어 반환

def fetch_exhibition_data(location, free_time):
    """ 사용자의 지역과 여가 시간에 맞는 전시회 데이터를 가져오는 함수 """
    API_KEY = os.getenv("EXHIBITION_API_KEY", "YOUR_TEST_API_KEY")
    sido = extract_sido(location)

    # 날짜 변환 (YYYY-MM-DD → YYYYMMDD)
    formatted_date = free_time.replace("-", "")

    params = {
        "serviceKey": API_KEY,
        "realmCode": "D000",
        "from": formatted_date,
        "to": formatted_date,
        "sido": sido,
        "pageNo": 1,
        "numOfRows": 10,
    }

    response = requests.get(API_URL, params=params)
    if response.status_code != 200:
        return {"code": "API_ERROR", "message": f"문화포털 API 요청 실패 (HTTP {response.status_code})"}

    try:
        data_dict = xmltodict.parse(response.text)
    except Exception as e:
        return {"code": "PARSE_ERROR", "message": f"XML 파싱 실패: {str(e)}"}

    if "response" not in data_dict or "body" not in data_dict["response"]:
        return {"code": "INVALID_RESPONSE", "message": "API 응답 구조가 예상과 다릅니다."}

    body = data_dict["response"]["body"]

    # 전시 데이터가 없을 경우 처리
    if body.get("totalCount") == "0":
        return {"code": "NF", "message": "No exhibition data found."}

    items = body.get("items", None)
    if not items or "item" not in items:  
        return {"code": "NF", "message": "No exhibition data found."}

    results = items["item"] if isinstance(items["item"], list) else [items["item"]]

    return {"code": "SU", "message": results}
