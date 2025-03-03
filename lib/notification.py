import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def send_discord_notification(message, is_error=False):
    """Discord webhook을 통해 알림을 보냅니다."""
    # 성공/실패에 따라 다른 webhook URL 사용
    webhook_url = os.getenv('DISCORD_ERROR_WEBHOOK_URL') if is_error else os.getenv('DISCORD_SUCCESS_WEBHOOK_URL')
    
    if not webhook_url:
        print("Discord webhook URL이 설정되지 않았습니다.")
        return
    
    korea_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 에러 여부에 따라 임베드 색상 및 아이콘 설정
    color = 0xFF0000 if is_error else 0x00FF00
    title_icon = "🚨" if is_error else "✅"
    
    data = {
        "embeds": [{
            "title": f"{title_icon} {'크롤링 에러 발생' if is_error else '크롤링 성공'}",
            "description": message,
            "color": color,
            "fields": [
                {
                    "name": "실행 시각",
                    "value": korea_time,
                    "inline": True
                }
            ],
            "footer": {
                "text": "KHU Menu Crawler"
            }
        }]
    }
    
    try:
        response = requests.post(
            webhook_url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        print(f"Discord 알림 전송 완료 ({'에러' if is_error else '성공'} 채널)")
    except requests.exceptions.RequestException as e:
        print(f"Discord 알림 전송 실패: {e}") 