import os
import dotenv
import requests
from json import dumps


def get_snippet(category: str, name: str, place: str, page: int=1) -> list:
    """
    google custom search api를 통해 여가 활동의 검색결과 중 미리보기(snippet) 부분을 List로 반환하는 함수.

    Args:
        category(str): 여가 활동의 카테고리
        name(str): 여가 활동의 이름
        place(str): 장소명/건물명(없을 경우 공백문자로 입력)
        page(int): 로드할 페이지의 수(default=1)

    Returns:
        list: 수집된 snippet들
    """
    start_page = page

    # 환경 변수에서 구글 검색 엔진과 google custom search API 키 불러오기
    dotenv.load_dotenv('config.env')
    Google_SEARCH_ENGINE_ID = os.getenv('Google_SEARCH_ENGINE_ID')
    Google_API_KEY = os.getenv('Google_API_KEY')

    if not Google_SEARCH_ENGINE_ID or not Google_API_KEY:
        return {
            "code": "CONFIG_ERROR",
            "message": "Google custom search API 키가 설정되지 않았습니다."
        }
    
    # 팝업스토어는 이름만 검색하도록 설정
    if category == '팝업스토어':
        query = name
    else:
        query = place + name

    url = f"https://www.googleapis.com/customsearch/v1?key={Google_API_KEY}&cx={Google_SEARCH_ENGINE_ID}&q={query}&start={start_page}"
    response = requests.get(url)

    if response.status_code == 200:
        snippets = [item['snippet'] for item in response.json()['items']]
        return dumps(snippets, ensure_ascii=False, indent=4)
        
    else:
        return {
            "code": "API_ERROR",
            "message": f"google custom search API 요청 실패: {response.status_code}"
        }
