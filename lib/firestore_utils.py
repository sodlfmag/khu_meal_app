# firestore_utils.py
import os
os.environ['GRPC_DNS_RESOLVER'] = 'native'  # gRPC 경고 메시지 제거
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

def get_current_links():
    """Firestore에서 현재 저장된 이미지 링크들을 가져옵니다."""
    try:
        db = firestore.Client()
        doc_ref = db.collection('menu_links').document('latest')
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            # 학생식당, 교직원식당, 푸드코트 순서로 링크 반환
            return [
                data.get('seoul_chungwoon', ''),
                data.get('seoul_puruensol', ''),
                data.get('global_studentunion', '')
            ]
        else:
            print("저장된 링크가 없습니다.")
            return ['', '', '']
            
    except Exception as e:
        print(f"링크 가져오기 실패: {e}")
        return ['', '', '']
