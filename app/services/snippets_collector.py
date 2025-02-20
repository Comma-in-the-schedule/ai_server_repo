import os
import requests

# 환경 변수에서 구글 커스텀 서치 API 키 불러오기
GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def get_snippet(category: str, title: str, place: str) -> dict:
    """
    Google Custom Search API를 사용하여 검색 스니펫을 가져오고, OpenAI API를 호출하여 설명을 생성하는 함수.

    Args:
        category(str): 여가 활동의 카테고리
        title(str): 여가 활동의 이름
        address(str): 장소명/건물명(없을 경우 공백문자로 입력)
        link(str): 네이버 API에서 가져온 원본 링크

    Returns:
        dict: OpenAI API에서 생성된 설명을 포함한 JSON 데이터
    """
    if not GOOGLE_SEARCH_ENGINE_ID or not GOOGLE_API_KEY:
        return {
            "code": "CONFIG_ERROR",
            "message": "Google Custom Search API 키가 설정되지 않았습니다."
        }
    
    # 검색어 설정
    query = title if category == "팝업스토어" else f"{place} {title}"
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_SEARCH_ENGINE_ID}&q={query}&start=1"

    response = requests.get(url)

    if response.status_code == 200:
        return {
        "code": "SU",
        "message": [item['snippet'] for item in response.json().get('items', []) if 'snippet' in item]
    }
    
    # return {
    #     "code": "API_ERROR",
    #     "message": f"Google Custom Search API 요청 실패: {response.status_code}"
    # }
    return {"code": "API_ERROR", "message": response}
