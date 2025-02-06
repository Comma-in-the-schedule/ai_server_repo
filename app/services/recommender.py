import os
import json
from openai import OpenAI
from dotenv import load_dotenv


def recommend(schedule:str, event_list:list[dict]) -> list[dict]:
    """
    openAI API를 통해 적절한 여가 활동을 추천하는 함수.

    Args:
        categorys(list): 선호 카테고리
        schedule(str): 가능한 시간
        event_list(list): json형식의 여가 활동 목록

    Returns:
        list: json형식의 추천 여가 활동 목록
    """
    load_dotenv('config.env')
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'),)


    prompt = f"""
    사용자의 여가 시간과 여가 활동 목록이 주어집니다.  
    운영 기간(`period`)과 운영 시간(`opening_time`)을 고려하여 여가 시간에 맞는 활동을 하나 추천하세요.  
    운영 기간(period)과 운영 시간(opening_time)의 형식은 여가 시간과 다를 수 있습니다.  
    예를 들어, 여가 시간은 'YYYY.MM.DD.-YYYY.MM.DD.' 형식으로 주어지지만,  
    운영 기간과 운영 시간은 'YY년 MM월 DD일부터 MM월 DD일까지'와 같은 형식일 수 있습니다.  
    추천할 활동은 반드시 제공된 여가 활동 목록 내에 존재해야 합니다.  

    ### 추천 우선순위:
    1. **운영 기간 및 운영 시간이 여가 시간과 일치하는 활동**
    2. **운영 기간이 여가 시간과 겹치는 활동** (운영 시간 데이터가 없을 경우 포함)
    3. **운영 기간이 명시되지 않은 활동**  

    운영 기간이 종료된 활동은 추천하지 않습니다.  

    #### 입력 예시
    - **사용자 여가 시간:** `{schedule}`  
    - **여가 활동 목록:** `{event_list}` (`json` 형식, `period` 및 `opening_time` 포함)  

    #### 출력 형식
    - 추천된 활동을 **제공된 JSON 형태 그대로 반환**합니다.  
    - 추천할 활동이 없을 경우 다음 JSON을 반환합니다:
    ```json
    "title": None 
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 json형태로 제공된 여러 여가 활동 중에서 사용자에게 가장 적합한 여가 활동을 추천하는 비서입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return json.loads(response.choices[0].message.content.lstrip('```json').rstrip('```'))
