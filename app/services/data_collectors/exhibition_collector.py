import requests
import xmltodict
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_coordinates(location):
    API_KEY = os.getenv("KAKAO_API_KEY")
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    params = {"query": location}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if response.status_code != 200:
        return {"code": "API_ERROR", "message": f"카카오 API 요청 실패 (HTTP {response.text})"}

    result = [float(data['documents'][0]['y']), float(data['documents'][0]['x'])]

    return {"code": "SU", "message": result}


def get_start_and_end_date(free_time):
    free_date = datetime.strptime(free_time.strip(), "%Y.%m.%d.")

    prev_date = free_date + relativedelta(months=-1)
    next_date = free_date + relativedelta(months=1)

    return prev_date.strftime("%Y%m%d"), next_date.strftime("%Y%m%d")


def fetch_exhibition_data(coordinates, free_time):
    """ 사용자의 지역과 여가 시간에 맞는 전시회 데이터를 가져오는 함수 """
    API_URL = "https://apis.data.go.kr/B553457/nopenapi/rest/publicperformancedisplays/realm"
    API_KEY = os.getenv("EXHIBITION_API_KEY", "YOUR_TEST_API_KEY")

    y, x = coordinates
    y_margin = 0.05
    x_margin = 0.05

    # 날짜 변환 (YYYY.MM.DD. → YYYYMMDD)
    start_date, end_date = get_start_and_end_date(free_time)
    params = {
        "serviceKey": API_KEY,
        "realmCode": "D000",
        "from": start_date,
        "to": end_date,
        "pageNo": 1,
        "numOfRows": 10,
        "gpsxfrom": x - x_margin,
        "gpsyfrom": y - y_margin,
        "gpsxto": x + x_margin,
        "gpsyto": y + y_margin
    }

    try:
        response = requests.get(API_URL, params=params)
    except requests.exceptions.SSLError as e:
        return {"code": "SSL ERROR", "message": "SSL 인증 실패"}
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
