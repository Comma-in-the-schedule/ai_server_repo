import os
import requests
from json import dumps
from app.services.openai_processor import generate_description  # OpenAI API 함수 추가

Google_SEARCH_ENGINE_ID = os.getenv('Google_SEARCH_ENGINE_ID')
Google_API_KEY = os.getenv('Google_API_KEY')

def get_snippet(category: str, name: str, address: str, link: str, page: int=1) -> dict:
    """
    Google Custom Search API를 사용하여 검색 스니펫을 가져오고, OpenAI API를 호출하여 설명을 생성하는 함수.

    Args:
        category(str): 여가 활동의 카테고리
        name(str): 여가 활동의 이름
        address(str): 장소명/건물명(없을 경우 공백문자로 입력)
        link(str): 네이버 API에서 가져온 원본 링크
        page(int): 로드할 페이지의 수(default=1)

    Returns:
        dict: OpenAI API에서 생성된 설명을 포함한 JSON 데이터
    """
    if not Google_SEARCH_ENGINE_ID or not Google_API_KEY:
        return {
            "code": "CONFIG_ERROR",
            "message": "Google Custom Search API 키가 설정되지 않았습니다."
        }
    
    # 검색어 설정
    query = name if category == "팝업스토어" else f"{address} {name}"
    url = f"https://www.googleapis.com/customsearch/v1?key={Google_API_KEY}&cx={Google_SEARCH_ENGINE_ID}&q={query}&start={page}"

    response = requests.get(url)

    if response.status_code == 200:
        snippets = [item['snippet'] for item in response.json().get('items', [])]

        # OpenAI API를 사용하여 설명 생성
        description_data = generate_description(
            category=category,
            title=name,
            address=address,
            link=link,  # 네이버 API에서 받은 원본 링크 사용
            snippets=snippets
        )

        return description_data
    
    return {
        "code": "API_ERROR",
        "message": f"Google Custom Search API 요청 실패: {response.status_code}"
    }
