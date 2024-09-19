import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# EPUB 파일에서 텍스트를 추출하는 함수
def extract_text_from_epub(epub_path, output_path):
    book = epub.read_epub(epub_path)
    all_text = []

    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            text = soup.get_text()
            all_text.append(text)

    # 추출한 텍스트를 파일에 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_text))

# 사용 예시
epub_path = 'pdftest/input/epub/alice.epub'  # EPUB 파일 경로
output_path = 'pdftest/input/epub_text.txt'  # 출력 파일 경로
extract_text_from_epub(epub_path, output_path)
