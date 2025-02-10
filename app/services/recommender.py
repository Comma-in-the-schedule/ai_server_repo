import os
import json
from openai import OpenAI

# OpenAI API 키 환경 변수 로드
openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=openai_api_key)

def recommend(free_time: str, event_list: list[dict]) -> dict:
    """
    OpenAI API를 통해 적절한 여가 활동을 추천하는 함수.

    Args:
        free_time (str): 사용자의 여가 가능 시간
        event_list (list[dict]): JSON 형식의 여가 활동 목록

    Returns:
        dict: 추천된 여가 활동 (없을 경우 "title": None 반환)
    """

    prompt = f"""
    사용자의 여가 시간과 여가 활동 목록이 주어집니다.  
    운영 기간('period')과 운영 시간('opening_time')을 고려하여 여가 시간에 맞는 활동을 하나 추천하세요.  
    추천할 활동은 반드시 제공된 여가 활동 목록 내에 존재해야 합니다.  

    ### 추천 우선순위:
    1. **운영 기간('period') 및 운영 시간('opening_time')이 여가 시간('free_time')과 일치하는 활동**
      - 기준에 부합하는 활동이 2개 이상일 경우 title이 여가 활동에 더 가까운 활동을 추천합니다.
    2. **운영 기간('period')이 여가 시간('free_time')과 겹치는 활동** (운영 시간 데이터가 없을 경우 포함)
    3. **운영 기간('period')이 명시되지 않은 활동**  

    운영 기간이 종료된 활동은 추천하지 않습니다.  
    여가 활동(팝업스토어, 전시회, 공연 등)과 전혀 연관성이 없어보이는 title은 제외하세요.
    - 예를 들어 서비스센터, 고객센터 등 '-센터'로 끝나는 이름은 여가 활동이 아닐 가능성이 높으니 제외하세요.
    **여가 시간('free_time')이 최종 추천 여가 활동의 운영 기간('period') 내에 포함되는지 반드시 확인하세요.**

    #### 입력 예시
    - **사용자 여가 시간:** `{free_time}`  
    - **여가 활동 목록:** `{event_list}` (`json` 형식, `period` 및 `opening_time` 포함)  

    #### 출력 형식
    - 추천된 활동을 **제공된 JSON 형태 그대로 반환**합니다.  
    - 추천할 활동이 없을 경우 다음 JSON을 반환합니다:
    ```json
    "title": "None"
    ```
    """


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 JSON 형태로 제공된 여러 여가 활동 중에서 사용자에게 가장 적합한 여가 활동을 추천하는 비서입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return json.loads(response.choices[0].message.content.lstrip('```json').rstrip('```'))
