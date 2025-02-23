# firestore_utils.py
from google.cloud import firestore

def save_links_to_firestore(links):
    """
    links 리스트의 첫 3개의 링크를 아래의 키로 Firestore에 저장합니다.
      - seoul_chungwoon : 1번째 링크
      - seoul_puruensol : 2번째 링크
      - global_studentunion : 3번째 링크
    Firestore의 "menu_links" 컬렉션 내 "latest" 문서에 저장합니다.
    """
    if len(links) < 3:
        print("링크가 3개 미만입니다. Firestore에 저장할 수 없습니다.")
        return
    
    db = firestore.Client()
    data = {
        "seoul_chungwoon": links[0],
        "seoul_puruensol": links[1],
        "global_studentunion": links[2]
    }
    
    doc_ref = db.collection("menu_links").document("latest")
    doc_ref.set(data)
    print("Firestore에 링크 저장 완료.")
