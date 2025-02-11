import os
import json
from openai import OpenAI
from datetime import datetime

# OpenAI API 키 환경 변수 로드
openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=openai_api_key)

def is_free_time_in_period(free_time: str, period: str) -> bool:
    """
    free_time은 ISO 형식의 날짜 (예: "2025-02-15" 또는 "2025-02-15T10:00:00")라고 가정하고,
    period는 "YYYY.MM.DD-YYYY.MM.DD" 형식으로 주어진다고 가정합니다.
    free_time이 period 내에 포함되면 True를 반환합니다.
    """
    try:
        # free_time에서 날짜 부분만 추출 (시간 정보는 무시)
        free_date = datetime.fromisoformat(free_time.split("T")[0])
        
        # period를 시작일과 종료일로 분리하여 파싱
        start_str, end_str = period.split("-")
        start_date = datetime.strptime(start_str.strip(), "%Y.%m.%d")
        end_date = datetime.strptime(end_str.strip(), "%Y.%m.%d")
        
        return start_date <= free_date <= end_date
    except Exception:
        # period 형식이 올바르지 않으면 False 반환
        return False

def recommend(free_time: str, event_list: list[dict]) -> dict:
    """
    OpenAI API를 통해 적절한 여가 활동을 추천하는 함수.

    Args:
        free_time (str): 사용자의 여가 가능 시간
        event_list (list[dict]): JSON 형식의 여가 활동 목록

    Returns:
        dict: 추천된 여가 활동 (없을 경우 "title": None 반환)
    """

    # 수정된 프롬프트: 날짜 처리 함수에 맞게 수정. free_time이 반드시 이벤트의 운영 기간에 포함되어야 한다는 조건을 명시합니다.
    prompt = f"""
    사용자의 여가 시간과 여가 활동 목록이 주어집니다.
    다음 조건을 반드시 만족하는 이벤트를 하나 추천하세요:
    1. **추천된 이벤트의 운영 기간(period)은 반드시 사용자 여가 시간(free_time)인 "{free_time.split("T")[0]}"을 포함해야 합니다.**
    2. 운영 기간이 종료된 이벤트는 제외합니다.
    3. 운영 시간(opening_time)이 free_time과 겹치는 경우 우선 추천합니다.
    4. 이벤트 목록은 반드시 제공된 JSON 형태의 목록에 있는 이벤트여야 합니다.
    5. 여가 활동과 관련 없는 이벤트(예: "서비스센터", "고객센터" 등)는 추천하지 않습니다.
    6. 만약 free_time을 포함하는 이벤트가 없다면 반드시 아래와 같이 "title": "None"을 반환해 주세요.

    #### 입력:
    - 사용자 여가 시간: "{free_time}"
    - 여가 활동 목록: {event_list}  (각 이벤트는 period 및 opening_time 포함)

    #### 출력 (반드시 JSON 형태로 응답):
    {{
        "category": "<카테고리>",
        "title": "<제목>",
        "description": "<설명>",
        "place": "<장소>",
        "address": "<주소>",
        "period": "<기간>",
        "opening_time": "<운영시간>",
        "url": "<링크>"
    }}

    만약 free_time을 포함하는 이벤트가 없다면, 반드시 다음과 같이 반환하세요:
    ```json
    {{ "title": "None" }}
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
