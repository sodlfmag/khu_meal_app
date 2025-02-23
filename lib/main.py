# main.py
import os
from dotenv import load_dotenv
from crawl import fetch_image_links
from firestore_utils import save_links_to_firestore

# .env 파일 로드 (여기에는 GOOGLE_APPLICATION_CREDENTIALS 경로가 설정되어 있어야 합니다)
load_dotenv()

if __name__ == "__main__":
    # 크롤링할 웹페이지 URL (실제 URL로 교체)
    url = "https://coop.khu.ac.kr/"  
    links = fetch_image_links(url)
    
    if links:
        print("크롤링된 링크:")
        for link in links:
            print(link)
        save_links_to_firestore(links)
    else:
        print("크롤링 결과가 없습니다.")
