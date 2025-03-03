# main.py
import os
from dotenv import load_dotenv
from crawl import fetch_image_links
from firestore_utils import save_links_to_firestore
from notification import send_discord_notification

# .env 파일 로드 (여기에는 GOOGLE_APPLICATION_CREDENTIALS 경로가 설정되어 있어야 합니다)
load_dotenv()

if __name__ == "__main__":
    try:
        # 크롤링할 웹페이지 URL
        url = "https://coop.khu.ac.kr/"
        links = fetch_image_links(url)
        
        if not links:
            error_msg = "크롤링 결과가 없습니다."
            print(error_msg)
            send_discord_notification(error_msg, is_error=True)
        elif len(links) < 3:
            error_msg = f"필요한 링크 수가 부족합니다. (발견된 링크 수: {len(links)})"
            print(error_msg)
            send_discord_notification(error_msg, is_error=True)
        else:
            print("크롤링된 링크:")
            for link in links:
                print(link)
            save_links_to_firestore(links)
            success_msg = f"크롤링 성공! {len(links)}개의 링크가 저장되었습니다.\n링크:\n" + "\n".join(links)
            send_discord_notification(success_msg, is_error=False)
            
    except Exception as e:
        error_msg = f"크롤링 중 오류 발생: {str(e)}"
        print(error_msg)
        send_discord_notification(error_msg, is_error=True)

