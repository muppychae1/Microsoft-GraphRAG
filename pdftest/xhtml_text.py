import os
import zipfile

def epub_to_xhtml(epub_file_path, output_dir):
    """EPUB 파일에서 XHTML 파일을 추출해 원본 그대로 TXT 파일로 저장하는 함수"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # EPUB 파일을 zip 파일로 열기
    with zipfile.ZipFile(epub_file_path, 'r') as epub_zip:
        # 모든 파일 리스트를 확인
        for file_name in epub_zip.namelist():
            # XHTML 파일만 처리
            if file_name.endswith('.xhtml'):
                # XHTML 파일 읽기
                with epub_zip.open(file_name) as xhtml_file:
                    xhtml_content = xhtml_file.read().decode('utf-8')  # 바이너리 데이터를 문자열로 변환
                    
                    # TXT 파일로 저장 (태그 포함)
                    txt_file_name = os.path.join(output_dir, os.path.basename(file_name).replace('.xhtml', '.txt'))
                    with open(txt_file_name, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(xhtml_content)
                        
                    print(f"Saved: {txt_file_name}")

# 사용 예시
epub_file = 'pdftest/input/epub/alice.epub'  # EPUB 파일 경로
output_directory = 'pdftest/input/text/alice'    # 출력할 디렉토리
epub_to_xhtml(epub_file, output_directory)
