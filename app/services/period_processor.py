from datetime import datetime


def is_free_time_in_period(free_time: str, period: str) -> bool:
    """
    free_time은 "YYYY.MM.DD."의 단일 날짜가 주어집니다.
    period는 "YYYY.MM.DD.-YYYY.MM.DD." 형식으로 주어집니다.
    free_time이 period 내에 포함되면 True를 반환합니다.
    """
    try:
        # free_time에서 날짜 부분만 추출 (시간 정보는 무시)
        free_date = datetime.strptime(free_time.strip(), "%Y.%m.%d.")
        
        # period를 시작일과 종료일로 분리하여 파싱
        start_str, end_str = period.split("-")
        start_date = datetime.strptime(start_str.strip(), "%Y.%m.%d.")
        end_date = datetime.strptime(end_str.strip(), "%Y.%m.%d.")
        
        return start_date <= free_date <= end_date
    except Exception:
        # period 형식이 올바르지 않으면 False 반환
        return False


def convert_to_period_format(start_date:str, end_date:str) -> str:
    """
    start_date와 end_date는 "YYYYMMDD"의 형식으로 주어집니다.
    start_date와 end_date를 "YYYY.MM.DD."의 형식으로 변환 후 "YYYY.MM.DD.-YYYY.MM.DD."으로 반환합니다.
    """
    if start_date != "미정":
        formatted_start_date = f'{start_date[:4]}.{start_date[4:6]}.{start_date[6:]}.'
    
    if end_date != "미정":
        formatted_end_date = f'{end_date[:4]}.{end_date[4:6]}.{end_date[6:]}.'

    return f'{formatted_start_date}-{formatted_end_date}'
