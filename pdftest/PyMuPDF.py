import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path, txt_path):
    # PDF 파일 열기
    doc = fitz.open(pdf_path)
    text = ""

    # 각 페이지에서 텍스트 추출
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()

    # 추출한 텍스트를 txt 파일에 덮어쓰기
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"텍스트가 {txt_path}에 저장되었습니다.")

# PDF 파일 경로와 저장할 txt 파일 경로 설정
pdf_file_path = "pdftest/input/금도끼와 은도끼.pdf"
text_file_path = "pdftest/input/PyMuPDF.txt"

# 함수 호출
extract_text_from_pdf(pdf_file_path, text_file_path)
