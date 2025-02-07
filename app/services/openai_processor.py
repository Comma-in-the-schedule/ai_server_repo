import os
import json
from openai import OpenAI

openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=openai_api_key)

def generate_description(category: str, title: str, address: str, link: str, snippets: list) -> dict:
    """
    OpenAI API를 통해 여가 활동에 대한 설명을 생성하는 함수.

    Args:
        category (str): 여가 활동의 카테고리
        title (str): 여가 활동의 이름
        address (str): 주소
        link (str): 네이버 API에서 가져온 링크
        snippets (list): Google Custom Search에서 수집한 snippet 리스트

    Returns:
        dict: OpenAI API로부터 생성된 설명을 포함한 JSON 데이터
    """
    prompt = f"""
    다음은 신뢰할 수 있는 {category} 정보와 Google 검색 API에서 반환된 snippet 목록입니다.  
    이 데이터를 바탕으로 아래 작업을 수행하세요.  

    ### **작업 내용**  
    1) snippet에서 신뢰할 수 있는 정보를 선별하여 간략한 설명('description')을 작성하세요.  
        - **title을 제외한 신뢰 가능한 데이터(예: 주소)는 설명에 포함하지 마세요.**  
        - 설명은 **snippet의 내용만을 기반으로 생성**해야 하며, 신뢰 가능한 정보와 일치하는 내용을 포함해야 합니다.  
        - 신뢰 가능한 데이터가 부족할 경우 snippet 간 교차 검증을 수행하세요.  
    2) 신뢰 가능한 정보 중 공백인 항목이 있다면, snippet에서 해당 정보를 찾아 알맞은 필드에 입력하세요.  
        - snippet에서 찾을 수 있다면 공백 대신 해당 값을 사용하세요.  
    3) 반환하기 전 설명('description')에 다른 필드의 데이터와 중복된 내용이 없는지 다시 한번 확인하세요.
        - **title을 제외한 신뢰 가능한 데이터(예: 주소)가 설명에 절대로 중복되지 않아야 합니다.**
        - 반환 시 홑따옴표(`)로 감싸지 마세요.

    ### **신뢰 가능한 데이터**  
        - **title**: {title}  
        - **address**: {address}    
        - **link**: {link}  

    ### **Snippet 목록**  
    {snippets}  

    ### **반환 형식 (JSON)**  
        "category": "{category}",
        "title": "{title}",
        "description": "작성한 설명 (title을 제외한 신뢰 가능한 정보는 포함하지 않음)",
        "address": "{address}",
        "link": "{link}"
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 한국어로 지정된 json 형식의 답변을 제공하는 유용한 비서입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return json.loads(response.choices[0].message.content.lstrip('```json').rstrip('```'))
