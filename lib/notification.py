import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def send_discord_notification(message, status="error"):
    """Discord webhook을 통해 알림을 보냅니다."""
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("Discord webhook URL이 설정되지 않았습니다.")
        return
    
    korea_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 상태에 따라 임베드 색상 및 아이콘 설정
    status_config = {
        "error": {"color": 0xFF0000, "icon": "🚨", "title": "크롤링 에러 발생"},
        "success_updated": {"color": 0x00FF00, "icon": "🔄", "title": "크롤링 성공 (메뉴 업데이트)"},
        "success_unchanged": {"color": 0x808080, "icon": "✅", "title": "크롤링 성공 (변경사항 없음)"}
    }
    
    config = status_config.get(status, status_config["error"])
    
    data = {
        "embeds": [{
            "title": f"{config['icon']} {config['title']}",
            "description": message,
            "color": config['color'],
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
        print(f"Discord 알림 전송 완료 ({config['title']})")
    except requests.exceptions.RequestException as e:
        print(f"Discord 알림 전송 실패: {e}") 