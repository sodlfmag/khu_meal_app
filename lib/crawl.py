# crawler.py
import requests
from bs4 import BeautifulSoup

def fetch_image_links(url):
    """
    지정된 URL의 페이지에서 class="elementor-element-99c8767"를 가진 section 내의
    모든 img 태그에서 실제 이미지 URL(data-src 또는 data-lazy-src, 없으면 src)을 추출합니다.
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
    src_list = []
    for img in img_tags:
        # lazy-loading 관련 속성 우선: data-src 또는 data-lazy-src, 없으면 src 사용
        actual_src = img.get("data-src") or img.get("data-lazy-src") or img.get("src")
        # placeholder data URI는 제외
        if actual_src and not actual_src.startswith("data:"):
            src_list.append(actual_src)
    return src_list
