def encode_euc_kr(text):
    """
    한글 텍스트를 EUC-KR URL 인코딩으로 변환합니다.
    """
    try:
        # 문자열을 EUC-KR로 인코딩
        encoded = text.encode('euc-kr')
        
        # URL 인코딩 (바이트를 %XX 형식으로 변환)
        result = ''.join(['%{:02X}'.format(byte) for byte in encoded])
        
        return result
    except Exception as e:
        print(f"인코딩 에러: {e}")
        return None

def decode_euc_kr(encoded_text):
    """
    EUC-KR URL 인코딩된 문자열을 원래 텍스트로 디코딩합니다.
    """
    try:
        # %XX 형식의 문자열을 바이트로 변환
        encoded_bytes = bytes.fromhex(encoded_text.replace('%', ''))
        
        # EUC-KR로 디코딩
        result = encoded_bytes.decode('euc-kr')
        
        return result
    except Exception as e:
        print(f"디코딩 에러: {e}")
        return None

# 사용 예시
if __name__ == "__main__":
    # 테스트할 한글 문자열들
    test_strings = ["테슬라", "미디어", "안녕하세요"]
    
    print("=== EUC-KR URL 인코딩/디코딩 테스트 ===")
    for text in test_strings:
        # 인코딩
        encoded = encode_euc_kr(text)
        print(f"\n원본 텍스트: {text}")
        print(f"인코딩 결과: {encoded}")
        
        # 디코딩
        if encoded:
            decoded = decode_euc_kr(encoded)
            print(f"디코딩 결과: {decoded}")
            
        # 원본과 디코딩 결과 비교
        if decoded == text:
            print("✓ 인코딩/디코딩 성공")
        else:
            print("✗ 인코딩/디코딩 실패")