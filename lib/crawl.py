import requests
from bs4 import BeautifulSoup

# 크롤링할 페이지 URL (실제 URL로 변경)
url = "https://coop.khu.ac.kr/"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # elementor-element-99c8767 클래스를 가진 section 태그 찾기
    section = soup.find("section", class_="elementor-element-99c8767")
    
    if section:
        img_tags = section.find_all("img")
        src_list = []
        for img in img_tags:
            # data-src나 data-lazy-src가 있으면 우선 사용
            actual_src = img.get("data-src") or img.get("data-lazy-src") or img.get("src")
            # data: 로 시작하면 placeholder 이므로 제외
            if actual_src and not actual_src.startswith("data:"):
                src_list.append(actual_src)
        
        if src_list:
            print("추출된 실제 이미지 URL 목록:")
            for src in src_list:
                print(src)
        else:
            print("실제 이미지 URL을 찾지 못했습니다.")
    else:
        print("section 태그를 찾지 못했습니다.")
else:
    print("페이지 요청 실패, 상태 코드:", response.status_code)