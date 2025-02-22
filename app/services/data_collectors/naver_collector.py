import requests
import os
import re

import dotenv

dotenv.load_dotenv('config.env')
# 환경 변수에서 네이버 API 키 불러오기
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def clean_html_tags(text):
    """HTML 태그 제거 함수"""
    clean = re.compile('<.*?>')  # HTML 태그를 찾는 정규식
    return re.sub(clean, '', text)

def collect_data(location, category):
    """
    사용자의 위치와 카테고리에 따라 네이버 지도 API를 통해 전시회/팝업스토어 데이터를 수집하는 함수.
    """
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        return {"code": "CONFIG_ERROR", "message": "네이버 API 키가 설정되지 않았습니다."}

    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    query = f"{location} {category}"
    url = f"https://openapi.naver.com/v1/search/local.json?query={query}&display=5"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = []

        for item in data.get("items", []):
            results.append({
                "title": clean_html_tags(item["title"]),
                "category": category,
                "address": item["roadAddress"],
                "link": item["link"]  # Google 검색 결과에 전달될 링크 정보 포함
            })
        
        return {"code": "SU", "message": results}

    return {"code": "API_ERROR", "message": f"네이버 지도 API 요청 실패: {response.status_code}"}


def get_address(place):
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        return {"code": "CONFIG_ERROR", "message": "네이버 API 키가 설정되지 않았습니다."}

    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    url = f"https://openapi.naver.com/v1/search/local.json?query={place}&display=1"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("items")[0]["roadAddress"]