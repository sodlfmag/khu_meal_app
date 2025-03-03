# crawler.py
import requests
from bs4 import BeautifulSoup

def is_valid_image_url(url):
    """이미지 URL이 유효한지 확인합니다."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def fetch_image_links(url):
    """
    지정된 URL의 페이지에서 class="elementor-element-99c8767"를 가진 section 내의
    유효한 이미지 URL만 추출합니다.
    """
    response = requests.get(url)
    if response.status_code != 200:
        print("페이지 요청 실패, 상태 코드:", response.status_code)
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    section = soup.find("section", class_="elementor-element-99c8767")
    if not section:
        print("해당 section 태그를 찾지 못했습니다.")
        return []
    
    img_tags = section.find_all("img")
    valid_src_list = []
    
    for img in img_tags:
        actual_src = img.get("data-src") or img.get("data-lazy-src") or img.get("src")
        if actual_src and not actual_src.startswith("data:"):
            if is_valid_image_url(actual_src):
                valid_src_list.append(actual_src)
                print(f"유효한 이미지 URL 발견: {actual_src}")
            else:
                print(f"유효하지 않은 이미지 URL 제외: {actual_src}")
    
    return valid_src_list
