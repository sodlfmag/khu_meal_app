# main.py
import os
from dotenv import load_dotenv
from crawl import fetch_image_links
from firestore_utils import save_links_to_firestore, get_current_links
from notification import send_discord_notification

# .env 파일 로드 (여기에는 GOOGLE_APPLICATION_CREDENTIALS 경로가 설정되어 있어야 합니다)
load_dotenv()

if __name__ == "__main__":
    try:
        # 크롤링할 웹페이지 URL
        url = "https://coop.khu.ac.kr/"
        new_links = fetch_image_links(url)
        
        if not new_links:
            error_msg = "크롤링 결과가 없습니다."
            print(f"[ERROR] {error_msg}")
            send_discord_notification(error_msg, "error")
        elif len(new_links) < 3:
            error_msg = f"필요한 링크 수가 부족합니다. (발견된 링크 수: {len(new_links)})"
            print(f"[ERROR] {error_msg}")
            send_discord_notification(error_msg, "error")
        else:
            # 현재 저장된 링크 가져오기
            current_links = get_current_links()
            
            if set(new_links) == set(current_links):
                # 변경사항이 없는 경우
                msg = "크롤링 완료. 메뉴 변경사항이 없습니다."
                print(f"[INFO] {msg}")
                send_discord_notification(msg, "success_unchanged")
            else:
                # 변경사항이 있는 경우
                changes = []
                menu_types = ["학생식당", "교직원식당", "푸드코트"]
                
                for i, (old, new) in enumerate(zip(current_links, new_links)):
                    if old != new:
                        changes.append(f"- {menu_types[i]}: 메뉴 업데이트")
                
                save_links_to_firestore(new_links)
                update_msg = "크롤링 완료. 다음 메뉴가 업데이트 되었습니다:\n" + "\n".join(changes)
                print(f"[INFO] {update_msg}")
                send_discord_notification(update_msg, "success_updated")
            
    except Exception as e:
        error_msg = f"크롤링 중 오류 발생: {str(e)}"
        print(error_msg)
        send_discord_notification(error_msg, "error")

